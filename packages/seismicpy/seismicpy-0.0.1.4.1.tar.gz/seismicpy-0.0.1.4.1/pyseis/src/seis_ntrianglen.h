#ifndef ntrianglen_h
#define ntrianglen_h

#include "seis_dtype.h"

void cntrianglen_init (int ndim  /* number of dimensions */, 
		      int *nbox /* triangle radius [ndim] */, 
		      int *ndat /* data dimensions [ndim] */,
		      float **len /* triangle lengths [ndim][nd] */,
                      int **sft /* triangle shifts [ndim][nd] */,
		      int repeat /* repeated smoothing */);
/*< initialize >*/


void cntrianglen_lop (bool adj, bool add, int nx, int ny, sp_complex* x, sp_complex* y);
/*< linear operator >*/


void cntrianglen_close(void);
/*< free allocated storage >*/

#endif
