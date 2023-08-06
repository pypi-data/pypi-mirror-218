#ifndef trianglen_h
#define trianglen_h

#include "seis_dtype.h"

void sp_ctrianglen_init (int ndim  /* number of dimensions */, 
			int *nbox /* triangle radius [ndim] */, 
			int *ndat /* data dimensions [ndim] */);
/*< initialize >*/


void sp_ctrianglen_lop (bool adj, bool add, int nx, int ny, sp_complex* x, sp_complex* y);
/*< linear operator >*/


void sp_ctrianglen_close(void);
/*< free allocated storage >*/

#endif

