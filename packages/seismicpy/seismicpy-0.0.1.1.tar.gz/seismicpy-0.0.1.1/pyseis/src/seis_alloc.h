

#ifndef KISS_FFT_H
#include "seis_kissfft.h"
#endif

#include "seis_dtype.h"

void *sp_alloc (size_t n    /* number of elements */, 
			  size_t size /* size of one element */);

float *sp_floatalloc (size_t n /* number of elements */);

float **sp_floatalloc2 (size_t n1 /* fast dimension */, 
				  size_t n2 /* slow dimension */);

float ***sp_floatalloc3 (size_t n1 /* fast dimension */, 
				   size_t n2 /* slower dimension */, 
				   size_t n3 /* slowest dimension */);

int *sp_intalloc (size_t n /* number of elements */);

int **sp_intalloc2 (size_t n1 /* fast dimension */, 
			      size_t n2 /* slow dimension */);

int ***sp_intalloc3 (size_t n1 /* fast dimension */, 
			       size_t n2 /* slower dimension */, 
			       size_t n3 /* slowest dimension */);
			       
// sp_complex *sp_complexalloc (size_t n /* number of elements */);

sp_complex *sp_complexalloc (size_t n /* number of elements */);

sp_complex **sp_complexalloc2 (size_t n1 /* fast dimension */, 
					 size_t n2 /* slow dimension */);

sp_complex ***sp_complexalloc3 (size_t n1 /* fast dimension */, 
					  size_t n2 /* slower dimension */, 
					  size_t n3 /* slowest dimension */);