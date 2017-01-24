#!/usr/bin/env python
# vim: fdm=marker fdl=0

import numpy as np
import sys
import locale

stdout_file_name = 'stdout'

def partition(total, num_part):#{{{
  """almost evenly split total into num_part
  """
  result = []
  least = int(total / num_part)

  for i in range(num_part):
    result.append(least)

  result[-1] += (total % num_part)

  return result
#}}}
def random_cluster(num_dim, mean_range, num_obs):#{{{
  """randomly create instances in a cluster

  :num_dim: # of dimensions
  :mean_range: mean_range[0] is low, and mean_range[1] is high
  :num_obs: # of observations
  :returns: multivariate normal distribution with num_obs instance

  """

  interval = mean_range[1] - mean_range[0]
  mean     = mean_range[0] + np.random.rand(num_dim) * interval
  cov      = np.diag(np.random.rand(num_dim) * interval)
  instance = np.random.multivariate_normal(mean, cov, num_obs)

  return instance
#}}}
def print_matrix(fp, matrix):#{{{
  """print the matrix in the list to stdout
  """

  for line in matrix:
    for item in line:
      fp.write('%f,' % item)
    fp.write('\n')
#}}}
def gendata(num_obs, num_dim, num_com, outfp, seed):#{{{
  """generate data as the input for the program  """

  instance = []


  # set seed
  np.random.seed(seed)

  num_obs_list = partition(num_obs, num_com)

  for i in range(num_com):
    mean_low   = i * 4
    mean_high  = mean_low + 2
    mean_range = [mean_low, mean_high]
    x          = random_cluster(num_dim, mean_range, num_obs_list[i])
    print_matrix(outfp, x)
#}}}

def main():
  """ If you change num_obs, num_dim and num_dim to arbitry value, the least
  likelybood might be nan. To get a more reasonable result, you may duplicate
  a set of small test data set and add some perturbation to them.

  The total number of observation would be num_dup * num_obs
  """

  num_dup  = 10000
  num_obs  = 100
  num_dim  = 3
  num_com  = 2
  out_path = "em-data-n%s-d%d-k%d.txt" % (locale.format("%d", num_dup * num_obs, grouping=True), num_dim, num_com)
  seed     = 10

  #outfilename = stdout_file_name
  outfilename = out_path
  if outfilename == stdout_file_name:
    outfp = sys.stdout
  else:
    outfp = open(outfilename, 'w')

  for i in range(num_dup):
    gendata(num_obs, num_dim, num_com, outfp, seed)

  outfp.close()

if __name__ == '__main__':
  main()
