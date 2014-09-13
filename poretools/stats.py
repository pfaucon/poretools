import statistics as stat
import Fast5File
import logging
from collections import defaultdict
logger = logging.getLogger('poretools')

def run(parser, args):
	if args.full_tsv:
		files = 0
		stats = defaultdict(list)
		for fast5 in Fast5File.Fast5FileSet(args.files):
			files += 1
			fas = fast5.get_fastas_dict()
			for category, fa in fas.iteritems():
				if fa is not None:
					stats[category].append(len(fa.seq))
					if category == 'twodirections':
						if fast5.is_high_quality():
							stats['2D_hq'].append(len(fa.seq))

			fast5.close()

		print "files\ttotal reads\t%d" % (files)

		for category in sorted(stats.keys()):
			sizes = stats[category]

			if len(sizes) > 0:
				print "%s\ttotal reads\t%d" % (category, len(sizes))
				print "%s\ttotal base pairs\t%d" % (category, sum(sizes))
				print "%s\tmean\t%.2f" % (category, stat.mean(sizes))
				print "%s\tmedian\t%d" % (category, stat.median(sizes))
				print "%s\tmin\t%d" % (category, min(sizes))
				print "%s\tmax\t%d" % (category, max(sizes))
			else:
				logger.warning("No valid sequences observed.\n")
	else:
		sizes = []
		for fast5 in Fast5File.Fast5FileSet(args.files):
			fas = fast5.get_fastas(args.type)
			sizes.extend([len(fa.seq) for fa in fas if fa is not None])
			fast5.close()

		if len(sizes) > 0:
			print "total reads\t%d" % (len(sizes))
			print "total base pairs\t%d" % (sum(sizes))
			print "mean\t%.2f" % (stat.mean(sizes))
			print "median\t%d" % (stat.median(sizes))
			print "min\t%d" % (min(sizes))
			print "max\t%d" % (max(sizes))
		else:
			logger.warning("No valid sequences observed.\n")
