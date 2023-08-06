#ifndef triangle_h
#define triangle_h

/*sp means seismic processing*/
// #include "_bool.h"
// #include "komplex.h"

#include "seis_dtype.h"


struct sp_Ctriangle {
    sp_complex *tmp;
    float wt;
    int np, nb, nx;
    bool box;
};

typedef struct sp_Ctriangle *sp_ctriangle;
/* abstract data type */
/*^*/


sp_ctriangle sp_ctriangle_init (int nbox /* triangle length */, 
				int ndat /* data length */,
				bool box /* if box instead of triangle */);
/*< initialize >*/


void sp_csmooth (sp_ctriangle tr    /* smoothing object */, 
		 int o, int d    /* trace sampling */, 
		 bool der        /* if derivative */,
		 sp_complex *x   /* data (smoothed in place) */);
/*< apply adjoint triangle smoothing >*/


void  sp_ctriangle_close(sp_ctriangle tr);
/*< free allocated storage >*/

#endif


