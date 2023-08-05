import pdb
import networkx as nx
import numpy as np
import pandas as pd
import pickle
from statsmodels.stats.multitest import multipletests
import scipy.stats as st
import matplotlib.pyplot as plt
import os
import copy
from collections import defaultdict
from tqdm import tqdm
import scanpy as sc
from scipy import sparse

from swan_vis.talon_utils import *

pd.options.mode.chained_assignment = None

def create_dupe_index(df, ind_name):
	"""
	Creates a duplicate column in the input DataFrame from the input column name

	Parameters:
		df (pandas DataFrame): DataFrame to create duplicate column
		ind_name (str): Name of column to duplicate

	Returns:
		df (pandas DataFrame): DataFrame with new duplicate column
	"""
	df[ind_name+'_back'] = df[ind_name]
	return df

def reset_dupe_index(df, ind_name):
	"""
	Reset index and rename duplicate index column

	Parameters:
		df (pandas DataFrame): DataFrame to reset index
		ind_name (str): Name of column to reset

	Returns:
		df (pandas DataFrame): DataFrame with reset duplicate index
	"""
	df.rename({ind_name: ind_name+'_back'}, inplace=True, axis=1)
	df.reset_index(inplace=True)
	return(df)

# set index, rename dupe index in df
def set_dupe_index(df, ind_name):
	"""
	Set duplicated column from create_dupe_index as the index and rename the
	duplicated column

	Parameters:
		df (pandas DataFrame): DataFrame to set index
		ind_name (str): Name of column to set as index

	Returns:
		df (pandas DataFrame): DataFrame with set duplicate index
	"""
	df.set_index(ind_name, inplace=True)
	df.rename({ind_name+'_back': ind_name}, inplace=True, axis=1)
	return(df)

def make_uns_key(kind, obs_col, obs_conditions, die_kind='iso'):
	"""
	Make a key name to reference die, det, or deg results in the .uns part of
	SwanGraph.adata.

	Parameters:
		kind (str): Choose 'det', 'die', 'deg' (for differential transcript,
			isoform switching / differential isoform expression,
			differential gene expression respectively)
		obs_col (str): Column name from self.adata.obs table to group on.
		obs_conditions (list of str, len 2): Which conditions from obs_col
			to compare? Required if obs_col has more than 2 unique values.
		die_kind (str): Which DIE test results. {'iso', 'tss', 'tes', 'ic'}
			Default: 'tss'

	Returns:
		uns_name (str): Name of .uns key
	"""
	if kind == 'die':
		kind = 'die_{}'.format(die_kind)

	uns_name = '{}_{}'.format(kind, obs_col)
	if obs_conditions:
		# sort arbitrarily for reproducibility regardless
		# of order conditions were passed in
		obs_conditions = sorted(obs_conditions)
		for cond in obs_conditions:
			uns_name += '_{}'.format(cond)
	return uns_name

def get_fields(fields):
	"""
	From the last column of a GTF, return a dictionary mapping each value.

	Parameters:
		fields (str): The last column of a GTF

	Returns:
		attributes (dict): Dictionary created from fields.
	"""

	attributes = {}

	description = fields.strip()
	description = [x.strip() for x in description.split(";")]
	for pair in description:
		if pair == "": continue

		pair = pair.replace('"', '')
		key, val = pair.split()
		attributes[key] = val

	# put in placeholders for important attributes (such as gene_id) if they
	# are absent
	if 'gene_id' not in attributes:
		attributes['gene_id'] = 'NULL'

	return attributes

def check_dir_loc(loc):
	"""
	Check if a directory exists. Raise an error if not.

	Parameters:
		loc (str): Directory name
	"""
	if '/' in loc:
		d = '/'.join(loc.split('/')[:-1])
		if not os.path.isdir(d):
			raise Exception('Directory {} is not found. '
				'Try a different save location'.format(d))

def check_file_loc(loc, ftype):
	"""
	Check if a file exists. Raises an error if not.

	Parameters:
	 	loc (str): File name
		ftype (str): File type
	"""
	if not os.path.isfile(loc):
		raise Exception('{} file not found at {}. '
			'Check path.'.format(ftype, loc))

# creates a file name based on input plotting arguments
def create_fname(prefix, indicate_dataset,
				 indicate_novel, browser,
				 ftype='summary', tid=None, gid=None):
	fname = prefix
	if indicate_dataset:
		fname += '_{}'.format(indicate_dataset)
	if indicate_novel:
		fname += '_novel'
	if browser:
		fname += '_browser'
	if tid:
		fname += '_{}'.format(tid)
	if gid:
		fname += '_{}'.format(gid)
	if ftype == 'summary':
		fname += '_summary.png'
	elif ftype == 'path':
		fname += '_path.png'
	elif ftype == 'report':
		fname += '_report.pdf'
	return fname

def gtf_or_db(fname):
	"""
	Determine if a file is GTF or TALON DB.

	Parameters:
		fname (str): File name / location

	Returns:
		ftype (str): 'gtf' or 'db' depending on results
	"""
	ext = fname.split('.')[-1]
	if ext == 'gtf': return 'gtf'
	elif ext == 'db': return 'db'
	else:
		raise Exception('File type must be gtf or db. '
			'Type received is {}'.format(ext))

# validate that a gtf has the correct fields and info in it
def validate_gtf(fname):
	"""
	Validates that the input GTF is valid input to Swan.

	Parameters:
		fname (str): Path / name of GTF file
	"""
	df = pd.read_csv(fname, sep='\t', usecols=[2,8], comment='#',
		names=['entry_type', 'fields'])
	if df.empty:
		raise Exception("GTF can't load correctly. Could be a header problem.")

	# first make sure that there are transcript and exon entries
	missing_entry_type = False
	missing_entry_types = []
	entry_types = df.entry_type.unique().tolist()
	if 'transcript' not in entry_types:
		missing_entry_type = True
		missing_entry_types.append('transcript')
	if 'exon' not in entry_types:
		missing_entry_type = True
		missing_entry_types.append('exon')
	if missing_entry_type:
		raise Exception('GTF is missing entry types {}'.format(missing_entry_types))

	# next check if gene_id, transcript_id, and gene_name fields exist
	# in each line of the thing
	df = df.loc[df.entry_type == 'transcript']
	df['tid'] = df.fields.str.extract(r'transcript_id "([A-z]+[0-9.]+)"',
		expand=False)
	df['gid'] = df.fields.str.extract(r'gene_id "([A-z]+[0-9.]+)"',
		expand=False)
	df.drop('fields', axis=1, inplace=True)

	missing_fields = []
	if df.tid.isnull().any():
		missing_fields.append('transcript_id')
	if df.gid.isnull().any():
		missing_fields.append('gene_id')
	if missing_fields:
		raise Exception('Last column of GTF is missing entry types {}'.format(missing_fields))

# depending on the strand, determine the start and stop
# coords of an intron or exon
def find_edge_start_stop(v1, v2, strand):
	"""
	Depending on the input strandedness, determine the start and stop
	coordinates of an edge

	Parameters:
		v1 (int): Coordinate of edge vertex
		v2 (int): Coordinate of edge vertex
		strand (str): Strand of edge

	Returns:
		start (int): Start coordinate of edge
		stop (int): Stop coordinate of edge
	"""
	if strand == '-':
		start = max([v1, v2])
		stop = min([v1, v2])
	elif strand == '+':
		start = min([v1, v2])
		stop = max([v1, v2])
	return start, stop

def reorder_exons(exon_ids):
	"""
	Reorder exons if they were out of order.

	Parameters:
		exon_ids (list of str): List of exons 'chrom_coord1_coord2_strand_exon'

	Returns:
		exons (list of str): List of same exon IDs ordered based on strand
			and genomic location
	"""
	strand = exon_ids[0].split('_')[-2]
	coords = [int(i.split('_')[-4]) for i in exon_ids]
	exons = sorted(zip(exon_ids, coords), key=lambda x: x[1])
	exons = [i[0] for i in exons]
	if strand == '-':
		exons.reverse()
	return exons

def get_ends(t_df, kind):
	"""
	From the transcript dataframe, return one with transcript id and tss / tes.

	Parameters:
		kind (str): Choose 'tss' or 'tes'
	"""
	# might be able to use this in the future:
	# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.explode.html
	if kind == 'tss':
		ind = 0
	elif kind == 'tes':
		ind = -1

	df = pd.DataFrame([[tid, path[ind]] for tid, path in \
		zip(t_df.index, t_df.loc_path)])
	df.columns = ['tid', 'vertex_id']
	df.set_index('tid', inplace=True)
	return df

def pivot_path_list(t_df, path_col):
	"""
	From the transcript dataframe, return a DataFrame with transcript id and
	edge/location ID for each edge/location in the path of that transcript.

	Parameters:
		t_df (pandas DataFrame): Transcript datafram from SwanGraph
		path_col (str): Which path to pull from. Choose from 'path' or 'loc_path'
	"""
	df = t_df.explode(path_col, ignore_index=False)
	if path_col == 'path':
		c = 'edge_id'
		c_map = {path_col: c}
	elif path_col == 'loc_path':
		c = 'vertex_id'
		c_map = {path_col: c}
	df.rename(c_map, axis=1, inplace=True)
	df = df[[c]]
	return df

##########################################################################
############### Related to calculating abundance values ##################
##########################################################################
def calc_total_counts(adata, obs_col='dataset', layer='counts'):
	"""
	Calculate cumulative expression per adata entry based on condition given
	by `obs_col`. Default column to use is `adata.obs` index column, `dataset`.

	Parameters:
		adata (anndata AnnData): Annotated data object from the SwanGraph
		obs_col (str): Column name from adata.obs table to group on.
			Default: 'dataset'
		layer (str): Layer of AnnData to pull from. Default = 'counts'

	Returns:
		df (pandas DataFrame): Pandas DataFrame where rows are the different
			conditions from `obs_col` and the columns are transcript ids in the
			SwanGraph, and values represent the cumulative counts per isoform
			per condition.

	"""

	# turn into a sparse dataframe
	cols = adata.var.index.tolist()
	inds = adata.obs[obs_col].tolist()
	data = adata.layers[layer].toarray()
	df = pd.DataFrame(data=data, index=inds, columns=cols)
	df.index.name = obs_col

	# add up values on condition (row)
	df = df.groupby(level=0).sum()

	# convert to sparse
	df = pd.DataFrame.sparse.from_spmatrix(data=sparse.csr_matrix(df.values),
										   index=df.index.tolist(),
										   columns=df.columns)

	return df

def calc_pi(adata, t_df, obs_col='dataset'):
	"""
	Calculate the percent isoform per gene per condition given by `obs_col`.
	Default column to use is `adata.obs` index column, `dataset`.

	Parameters:
		adata (anndata AnnData): Annotated data object from the SwanGraph
		t_df (pandas DataFrame): Pandas Dataframe that has index to
			gene id mapping
		obs_col (str): Column name from adata.obs table to group on.
			Default: 'dataset'

	Returns:
		df (pandas DataFrame): Pandas DataFrame where rows are the different
			conditions from `obs_col` and the columns are transcript ids in the
			SwanGraph, and values represent the percent isoform usage per gene
			per condition.
		sums (pandas DataFrame): Pandas DataFrame where rows are the different
			conditions from `obs_col` and the columns are transcript ids in the
			SwanGraph, and values represent the cumulative counts per isoform
			per condition.
	"""

	# calculate cumulative counts across obs_col
	id_col = adata.var.index.name
	conditions = adata.obs[obs_col].unique().tolist()
	df = calc_total_counts(adata, obs_col=obs_col)
	df = df.transpose()

	# we use ints to index edges and locs
	if id_col == 'vertex_id' or id_col == 'edge_id':
		df.index = df.index.astype('int')

	sums = df.copy(deep=True)
	sums = sums[conditions]
	sums = sums.transpose()

	# add gid
	df = df.merge(t_df['gid'], how='left', left_index=True, right_index=True)
	t_counts = df.melt(id_vars=['gid'],
					   value_vars=conditions,
					   var_name=obs_col,
					   value_name='t_counts',
					   ignore_index=False)
	t_counts.index.name = id_col
	t_counts.reset_index(inplace=True)

	# calculate total number of reads per gene per condition
	temp = df.copy(deep=True)
	temp.reset_index(drop=True, inplace=True)
	temp[conditions] = temp[conditions].sparse.to_dense()
	totals = temp.groupby('gid').sum().reset_index()

	# merge back in
	df = df.copy(deep=True)
	df.reset_index(inplace=True)
	df.rename({'index':id_col}, axis=1, inplace=True)
	df = df.merge(totals, on='gid', suffixes=('_t_counts', None))
	del totals

	df = df.melt(id_vars=['gid'],
				 value_vars=conditions,
				 var_name=obs_col,
				 value_name='gene_counts')
	df = df.drop_duplicates()
	df = t_counts.merge(df, how='left', on=['gid', obs_col])

	df['pi'] = (df.t_counts/df.gene_counts)*100
	df = df.pivot(columns=obs_col, index=id_col, values='pi')

	# order based on order in adata
	ids = adata.var.index.tolist()
	df = df.loc[ids]
	cols = adata.obs[obs_col].unique().tolist()
	df = df[cols]

	# convert to sparse
	df = df.transpose()
	df = pd.DataFrame.sparse.from_spmatrix(data=sparse.csr_matrix(df.values),
										   index=df.index.tolist(),
										   columns=df.columns)
	return df, sums

def calc_tpm(adata, obs_col='dataset', how='mean', recalc=False):
	"""
	Calculate the TPM per condition given by `obs_col`.
	Default column to use is `adata.obs` index column, `dataset`.

	Parameters:
		adata (anndata AnnData): Annotated data object from the SwanGraph
		obs_col (str or list of str): Column name from adata.obs table to group on.
			Default: 'dataset'
		how (str): How to compute tpm across multiple datasets {'mean', 'max'}
		recalc (bool): Whether tpm data should be recalculated or tpm
			values should just be averaged
			Default: False

	Returns:
		df (pandas DataFrame): Pandas datafrom where rows are the different
			conditions from `obs_col` and the columns are transcript ids in the
			SwanGraph, and values represent the TPM value per isoform per
			condition.
	"""

	# only need to calculate tpm once when adding abundance
	if recalc:

		# calculate tpm using scanpy
		d = sc.pp.normalize_total(adata,
								  layer='counts',
								  target_sum=1e6,
								  key_added='total_counts',
								  inplace=False)
		adata.obs['total_counts'] = d['norm_factor']
		data = d['X'].toarray()

	# otherwise just grab the tpm from the adata
	else:
		data = adata.layers['tpm'].toarray()

	# turn into a dataframe
	cols = adata.var.index.tolist()
	inds = adata.obs[obs_col].tolist()
	df = pd.DataFrame(data=data, columns=cols, index=inds)
	df.index.name = obs_col

	# average across tpm
	if obs_col != 'dataset':

		# keep track of original row order to sort by
		row_order = df.index.unique().tolist()
		row_map = {}
		for i, row in enumerate(row_order):
			row_map[row] = i

		df['row_order'] = df.index.map(row_map)
		df.reset_index(inplace=True)
		if how == 'mean':
			df = df.groupby(obs_col).mean()
		elif how == 'max':
			df = df.groupby(obs_col).max()
		df = df.sort_values(by='row_order', ascending=True)
		df.drop('row_order', inplace=True, axis=1)

	# make sparse
	data = sparse.csr_matrix(df.values)
	inds = df.index.tolist()
	cols = df.columns.tolist()
	df = pd.DataFrame.sparse.from_spmatrix(data, index=inds, columns=cols)

	return df

##########################################################################
####################### Related to file parsing ##########################
##########################################################################

def get_stable_gid(df, col):
	"""
	Get a list of stable gene ids from a dataframe

	Parameters:
		df (pandas DataFrame): DF w/ ENSEMBL gids in some column
		col (str): Column name of gids

	Returns:
		gids (list of str): List of stable gids
	"""
	df = df.copy(deep=True)
	try:
		df[['temp', 'par_region_1', 'par_region_2']] = df[col].str.split('_', n=2, expand=True)
		df[col] = df[col].str.split('.', expand=True)[0]
		df[['par_region_1', 'par_region_2']] = df[['par_region_1',
														   'par_region_2']].fillna('')
		df[col] = df[col]+df.par_region_1+df.par_region_2
		df.drop(['temp', 'par_region_1', 'par_region_2'], axis=1, inplace=True)
	except:
		df[col] = df[col].str.split('.', expand=True)[0]

	return df[col].tolist()

def parse_db(database, pass_list, observed, include_isms, verbose):
	"""
	Get the unique transcripts and exons that are present in a TALON DB
	transcriptome.

	Parameters:
		database (str): Path to database file
		pass_list (str): Path to TALON pass list files
		observed (bool): Whether or not to only use observed transcripts
		include_isms (bool): Whether to include ISMs or not
		verbose (bool): Display progress

	Returns:
		t_df (pandas DataFrame): DataFrame of transcripts in TALON db. Index
			is transcript ids. Columns are gene id, gene name,
			transcript id (same as key), transcript name, strand, and exons
			belonging to the transcript.
		exon_df (pandas DataFrame): DataFrame of exons in TALON db. Index is exon ids
			which consist of chromosome_v1_v2_strand_exon. Columns are edge id
			(same as key), chromosome, v1, v2, strand, and edge type
			(all exon in this case) of each exon.
	"""

	# make sure files exist
	if pass_list:
		check_file_loc(pass_list, 'pass list')

	# annot = check_annot_validity(annot, database)

	pass_list = handle_filtering(database, observed, pass_list)

	# create separate gene and transcript pass_lists
	gene_pass_list = []
	transcript_pass_list = []
	for key,group in itertools.groupby(pass_list,operator.itemgetter(0)):
		gene_pass_list.append(key)
		for id_tuple in list(group):
			transcript_pass_list.append(id_tuple[1])

	# get gene, transcript, and exon annotations
	gene_annotations = get_annotations(database, "gene",
									   pass_list = gene_pass_list)
	transcript_annotations = get_annotations(database, "transcript",
											 pass_list = transcript_pass_list)
	exon_annotations = get_annotations(database, "exon")

	# get transcript data from the database
	gene_2_transcripts = get_gene_2_transcripts(database,
						 transcript_pass_list)

	# get exon location info from database
	exon_ID_2_location = fetch_exon_locations(database)

	transcripts = {}
	exons = {}

	if verbose:
		n_transcripts = len(transcript_pass_list)
		pbar = tqdm(total=n_transcripts)
		pbar.set_description('Processing transcripts')

	# loop through genes, transcripts, and exons
	for gene_ID, transcript_tuples in gene_2_transcripts.items():
		curr_annot = gene_annotations[gene_ID]
		gene_annotation_dict = {}
		for annot in curr_annot:
			attribute = annot[3]
			value = annot[4]
			gene_annotation_dict[attribute] = value

		# check if there's a gene name field and add one if not
		if 'gene_name' not in gene_annotation_dict:
			gene_annotation_dict['gene_name'] = gene_annotation_dict['gene_id']

		# get transcript entries
		for transcript_entry in transcript_tuples:
			transcript_ID = transcript_entry["transcript_ID"]

			curr_transcript_annot = transcript_annotations[transcript_ID]

			transcript_annotation_dict = {}
			for annot in curr_transcript_annot:
				attribute = annot[3]
				value = annot[4]
				transcript_annotation_dict[attribute] = value


			if 'transcript_name' not in transcript_annotation_dict:
				transcript_annotation_dict['transcript_name'] = transcript_annotation_dict['transcript_id']
			tid = transcript_annotation_dict['transcript_id']
			tname = transcript_annotation_dict['transcript_name']
			gid = gene_annotation_dict['gene_id']
			gname = gene_annotation_dict['gene_name']
			strand = transcript_entry['strand']

			novelty = get_transcript_novelties(transcript_annotation_dict)

			# add transcript to dictionary
			entry = {'gid': gid,
					 'gname': gname,
					 'tid': tid,
					 'tname': tname,
					 'strand': strand,
					 'novelty': novelty,
					 'exons': []}
			transcript = {tid: entry}
			transcripts.update(transcript)

			if verbose:
				pbar.update(1)

			if transcript_entry["n_exons"] != 1:
				transcript_edges = [str(transcript_entry["start_exon"])] + \
								   str(transcript_entry["jn_path"]).split(",")+ \
								   [str(transcript_entry["end_exon"])]
			else:
				transcript_edges = [transcript_entry["start_exon"]]

			# get exon entries
			for exon_ID in transcript_edges[::2]:
				exon_ID = int(exon_ID)
				curr_exon_annot = exon_annotations[exon_ID]

				exon_annotation_dict = {}
				for annot in curr_exon_annot:
					attribute = annot[3]
					value = annot[4]
					exon_annotation_dict[attribute] = value

				e_tuple = exon_ID_2_location[exon_ID]
				chrom = e_tuple[0]
				start = e_tuple[1]
				stop = e_tuple[2]
				strand = e_tuple[3]
				start, stop = find_edge_start_stop(start, stop, strand)
				eid = '{}_{}_{}_{}_exon'.format(chrom, start, stop, strand)

				# add novel exon to dictionary
				if eid not in exons:
					edge = {eid: {'eid': eid,
								  'chrom': chrom,
								  'v1': start,
								  'v2': stop,
								  'strand': strand}}
					exons.update(edge)

				# add this exon to the transcript's list of exons
				if tid in transcripts:
					transcripts[tid]['exons'].append(eid)

	t_df = pd.DataFrame(transcripts).transpose()
	exon_df = pd.DataFrame(exons).transpose()

	# use stable gid if we can
	try:
		t_df['gid'] = get_stable_gid(t_df, 'gid')
	except:
		pass

	return t_df, exon_df

def parse_gtf(gtf_file, include_isms, verbose):
	"""
	Get the unique transcripts and exons that are present in a GTF
	transcriptome.

	Parameters:
		gtf_file (str): File path of GTF
		include_isms (bool): Whether to include ISMs or not
		verbose (bool): Display progress

	Returns:
		t_df (pandas DataFrame): DataFrame of transcripts in GTF. Index
			is transcript ids. Columns are gene id, gene name,
			transcript id (same as key), transcript name, strand, and exons
			belonging to the transcript.
		exon_df (pandas DataFrame): DataFrame of exons in GTF. Index is exon ids
			which consist of chromosome_v1_v2_strand_exon. Columns are edge id
			(same as key), chromosome, v1, v2, strand, and edge type
			(all exon in this case) of each exon.
		from_talon (bool): Whether or not the GTF was determined to be
			from TALON
		from_cerberus (bool): Whether or not the GTF is from cerberus
	"""

	# counts the number of transcripts in a given GTF
	# so that we can track progress
	def count_transcripts(gtf_file):
		df = pd.read_csv(gtf_file, sep='\t', usecols=[2],
			names=['entry_type'], comment='#')
		df = df.loc[df.entry_type == 'transcript']
		n = len(df.index)
		return n

	# get the number of transcripts in the file
	n_transcripts = count_transcripts(gtf_file)

	# dictionaries to hold unique edges and transcripts
	transcripts = {}
	exons = {}
	from_talon = False
	from_cerberus = False
	ism_tids = []

	# display progess
	if verbose:
		pbar = tqdm(total=n_transcripts)
		counter = 0

	with open(gtf_file) as gtf:
		for line in gtf:

			# ignore header lines
			if line.startswith('#'):
				continue

			# split each entry
			line = line.strip().split('\t')

			# get some fields from gtf that we care about
			chrom = line[0]
			entry_type = line[2]
			start = int(line[3])
			stop = int(line[4])
			strand = line[6]
			fields = line[-1]

			# transcript entry
			if entry_type == "transcript":

				# update progress bar
				if verbose:
					counter+=1
					if counter % 100 == 0:
						pbar.update(100)
						pbar.set_description('Processing transcripts')

				attributes = get_fields(fields)

				# check if this gtf has transcript novelty vals
				# for the first transcript entry
				if not transcripts:
					if 'talon_transcript' in attributes or 'talon_gene' in attributes:
						from_talon = True
					if 'ic_id' in attributes:
						from_cerberus = True

				tid = attributes['transcript_id']
				gid = attributes['gene_id']

				# check if there's a gene/transcript name field and
				# add one if not
				if 'gene_name' not in attributes:
					attributes['gene_name'] = attributes['gene_id']
				if 'transcript_name' not in attributes:
					attributes['transcript_name'] = attributes['transcript_id']

				gname = attributes['gene_name']
				tname = attributes['transcript_name']

				# add transcript to dictionary
				entry = {'gid': gid,
						 'gname': gname,
						 'tid': tid,
						 'tname': tname,
						 'strand': strand,
						 'exons': []}

				# if we're using a talon gtf, add a novelty field
				if from_talon:
					novelty = get_transcript_novelties(attributes)
					entry['novelty'] = novelty
				if from_cerberus:
					entry['tss_id'] = attributes['tss_id']
					entry['tes_id'] = attributes['tes_id']
					entry['ic_id'] = attributes['ic_id']

				# do not include ISM transcripts
				if not include_isms and from_talon:
					if novelty == 'ISM':
						ism_tids += [tid]
				# else:
					# transcript = {tid: entry}
					# transcripts.update(transcript)
				transcript = {tid: entry}
				transcripts.update(transcript)

			# exon entry
			elif entry_type == "exon":
				attributes = get_fields(fields)
				start, stop = find_edge_start_stop(start, stop, strand)
				eid = '{}_{}_{}_{}_exon'.format(chrom, start, stop, strand)
				tid = attributes['transcript_id']

				# add novel exon to dictionary
				if eid not in exons:
					edge = {eid: {'eid': eid,
								  'chrom': chrom,
								  'v1': start,
								  'v2': stop,
								  'strand': strand,
								  'edge_type': 'exon'}}

					# don't include exons that come from ISM transcripts
					if not include_isms and from_talon:
						if transcripts[tid]['novelty'] == 'ISM':
							pass
						else:
							exons.update(edge)
					else:
						exons.update(edge)

				# add this exon to the transcript's list of exons
				if tid in transcripts:
					transcripts[tid]['exons'].append(eid)

	t_df = pd.DataFrame(transcripts).transpose()
	exon_df = pd.DataFrame(exons).transpose()

	# remove ISMs that we've recorded
	if not include_isms:
		t_df = t_df.loc[~t_df.tid.isin(ism_tids)]

	# use stable gid if we can
	try:
		t_df['gid'] = get_stable_gid(t_df, 'gid')
	except:
		pass

	return t_df, exon_df, from_talon, from_cerberus

##########################################################################
######################## Related to DIE testing ##########################
##########################################################################

def get_die_gene_table(gene_df, conditions, rc):
	"""
	Creates a length n (max 11) table ready for DIE testing for a given gene.
	Returns None for genes deemed untestable if there aren't enough reads per
	condition or if the gene only has one isoform. Removes isoforms that are
	unexpressed in both conditions. Aggregates the counts for the
	lowest-expressed isoforms (11+). Calculates dpi (change in percent isoform
	usage) between conditions.

	Parameters:
		gene_df (pandas DataFrame): DataFrame of transcript counts and percent
			isoform expression per isoform of one gene.
		conditions (list of str, len 2): Names of 2 conditions being tested
		rc (int): Number of reads needed per gene per condition for testing

	Returns:
		gene_df (pandas DataFrame): :ength n table of counts per isoform per
			condition, percent isoform per gene per condition, and change in
			percent isoform across conditions IF the gene is testable
		test_result (str): Reason why gene was untestable, if relevant
	"""

	id_col = 'tid'
	gene_df.sort_values(by='total_counts', ascending=False, inplace=True)

	# limit to just isoforms with > 0 expression in at least one condition
	cond1 = conditions[0]
	cond2 = conditions[1]
	gene_df = gene_df.loc[(gene_df[cond1]>0)|(gene_df[cond2]>0)]

	# limit to genes with more than 1 isoform expressed
	if len(gene_df.index) <= 1:
		test_result = '1_iso'
		return None, test_result

	# if there are more than 11 isoforms, agg. the n - 11 least expressed
	# isoforms into one
	if len(gene_df.index) > 11:
		gene_df.reset_index(inplace=True)

		temp = gene_df.iloc[10:].sum()
		temp[id_col] = 'all_other'
		temp['gid'] = gene_df.gid.unique().tolist()[0]
		temp.index.name = None
		temp = pd.DataFrame(temp).transpose()

		gene_df = gene_df.iloc[:10]
		gene_df = pd.concat([gene_df, temp])
		gene_df.set_index('tid', inplace=True)

	# does this gene reach the desired read count threshold?
	for cond in conditions:
		counts_col = cond+'_counts'
		if gene_df[counts_col].sum() < rc:
			test_result = 'below_rc'
			return None, test_result

	# only do the rest if there's something left
	if gene_df.empty:
		test_result = 'both_0_exp'
		return None, test_result

	# compute isoform-level and gene-level delta pis
	# gene_df[cond1] = gene_df[cond1].astype(float)
	# gene_df[cond2] = gene_df[cond2].astype(float)
	gene_df[cond1] = gene_df[cond1].values.to_dense().astype(np.float64)
	gene_df[cond2] = gene_df[cond2].values.to_dense().astype(np.float64)
	gene_df['dpi'] = gene_df[cond1] - gene_df[cond2]
	test_result = 'testable'

	return gene_df, test_result

def test_gene(gene_df, conditions):
	"""
	Performs a chi-squared test between two conditions on their read counts.
	Also calculates the gene's DPI, or change in percent isoform as the sum of
	either the top two positive changes or top two negative changes (whichever
	is greater in magnitude).

	Parameters:
		gene_df (pandas DataFrame): Output from get_die_gene_table.
		conditions (list of str, len 2): Name of condition columns

	Returns:
		entry (list): List of gene id, gene dpi, and information about top 2 pos
			and neg dpis
	"""

	counts_cols = [c+'_counts' for c in conditions]

	# get highest 2 positive dpis
	temp = gene_df.sort_values(by='dpi', ascending=False)
	temp = temp.loc[temp.dpi > 0]

	# if there are fewer than 2 isoforms
	temp_len = len(temp.index)
	if temp_len >= 2:
		pos_dpi = temp.iloc[:2].dpi.sum(axis=0)
		pos_isos = temp.iloc[:2].index.tolist()
		pos_dpis = temp.iloc[:2].dpi.tolist()
	else:
		pos_dpi = temp.dpi.sum(axis=0)
		pos_isos = temp.index.tolist()+[np.nan for i in range(temp_len, 2)]
		pos_dpis = temp.dpi.tolist()+[np.nan for i in range(temp_len, 2)]

	# get highest 2 negative dpis
	temp = gene_df.sort_values(by='dpi', ascending=True)
	temp = temp.loc[temp.dpi < 0]

	# if there are fewer than 2 isoforms
	temp_len = len(temp.index)
	if temp_len >= 2:
		neg_dpi = abs(temp.iloc[:2].dpi.sum(axis=0))
		neg_isos = temp.iloc[:2].index.tolist()
		neg_dpis = temp.iloc[:2].dpi.tolist()
	else:
		neg_dpi = abs(temp.dpi.sum(axis=0))
		neg_isos = temp.index.tolist()+[np.nan for i in range(temp_len, 2)]
		neg_dpis = temp.dpi.tolist()+[np.nan for i in range(temp_len, 2)]

	gene_dpi = max(pos_dpi, neg_dpi)

	# chi squared test
	chi_table = gene_df[counts_cols].to_numpy()
	chi2, p, dof, exp = st.chi2_contingency(chi_table)

	entry = [p, gene_dpi]+pos_isos+pos_dpis+neg_isos+neg_dpis

	return entry

# turn a list of dataset groups and names for those groups into a
# dictionary
def make_cond_map(groups, group_names):
	cond_map = dict()
	for group, group_name in zip(groups, group_names):
		if type(group) == list:
			for group_item in group:
				cond_map[group_item] = group_name
		else:
			cond_map[group] = group_name
	return cond_map

# get novelty types associated with each transcript
def get_transcript_novelties(fields):
	if 'transcript_status' in fields.keys():
		if fields['transcript_status'] == 'KNOWN':
			return 'Known'

	if 'ISM_transcript' in fields:
		return 'ISM'
	elif 'NIC_transcript' in fields:
		return 'NIC'
	elif 'NNC_transcript' in fields:
		return 'NNC'
	elif 'antisense_transcript' in fields:
		return 'Antisense'
	elif 'intergenic_transcript' in fields:
		return 'Intergenic'
	elif 'genomic_transcript' in fields:
		return 'Genomic'
	else:
		return 'Undefined'

# reformat talon abundance file for the generic format expected by swan
def reformat_talon_abundance(df, how='iso', ofile=None):
	"""
	Reformat TALON abundance file into the format expected by add_abundance.
	Removes all columns but the annot_transcript_id column and counts columns.

	Parameters:
		df (pandas DataFrame): DF representation of TALON abundance
		ofile (str): Filename to save output to, if any.
			Default: None

	Returns:
		df (pandas DataFrame): DataFrame of abundance values indexed by
			transcript ID
	"""

	drop_cols = ['gene_ID', 'transcript_ID', 'annot_gene_name',
		'annot_transcript_name', 'n_exons', 'length', 'gene_novelty',
		'transcript_novelty', 'ISM_subtype']
	if how=='iso':
		drop_cols.append('annot_gene_id')
	elif how=='gene':
		drop_cols.append('annot_transcript_id')

	# drop the drop cols that exist in this df
	# (ignore key errors)
	df.drop(drop_cols,
			axis=1,
			inplace=True,
			errors='ignore')

	# if not writing output file just return df
	if not ofile:
		return df

	# otherwise dump to output file
	df.to_csv(ofile, sep='\t', index=False)

def read(file):
	"""
	Read a SwanGraph from a saved pickle file.

	Parameters:
		file (str): Name / path to saved Swan file

	Returns:
		sg (SwanGraph): SwanGraph stored in file
	"""
	check_file_loc(file, 'SwanGraph')
	picklefile = open(file, 'rb')
	sg = pickle.load(picklefile)

	print('Read in graph from {}'.format(file))
	return sg

# saves current figure named oname. clears the figure space so additional
# plotting can be done
def save_fig(oname):
	"""
	Save the current figure as a png with a given file prefix.

	Parameters:
		oname (str): Path / prefix to saved image
	"""
	check_dir_loc(oname)
	plt.axis('off')
	# plt.tight_layout()
	plt.savefig(oname, format='png', dpi=300, bbox_inches='tight')
	plt.clf()
	plt.close()
