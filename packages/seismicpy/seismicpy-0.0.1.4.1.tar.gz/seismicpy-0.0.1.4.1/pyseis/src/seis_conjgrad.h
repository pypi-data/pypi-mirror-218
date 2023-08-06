#ifndef _conjgrad_h
#define _conjgrad_h

#include "seis_dtype.h"
#include <stdbool.h>

// #include "_bool.h"
// #include "c99.h"
// #include "_solver.h"

/*below is from _solver.h */
typedef void (*sp_operator)(bool,bool,int,int,float*,float*);
typedef void (*sp_solverstep)(bool,int,int,float*,
			   const float*,float*,const float*);
typedef void (*sp_weight)(int,const float*,float*);
/*^*/

typedef void (*sp_coperator)(bool,bool,int,int,sp_complex*,sp_complex*);
typedef void (*sp_csolverstep)(bool,int,int,sp_complex*,
			       const sp_complex*,sp_complex*,
			       const sp_complex*);
typedef void (*sp_cweight)(int,const sp_complex*,float*);
/*above is from _solver.h */

void sp_adjnull (bool adj /* adjoint flag */, 
		 bool add /* addition flag */, 
		 int nx   /* size of x */, 
		 int ny   /* size of y */, 
		 float* x, 
		 float* y);
/*< Zeros out the output (unless add is true). 
  Useful first step for any linear operator. >*/
  
void sp_cadjnull (bool adj /* adjoint flag */, 
		  bool add /* addition flag */, 
		  int nx   /* size of x */, 
		  int ny   /* size of y */, 
		  sp_complex* x, 
		  sp_complex* y);
/*< adjnull version for complex data. >*/


void sp_cconjgrad_init(int np1     /* preconditioned size */, 
		       int nx1     /* model size */, 
		       int nd1     /* data size */, 
		       int nr1     /* residual size */, 
		       float eps1  /* scaling */,
		       float tol1  /* tolerance */, 
		       bool verb1  /* verbosity flag */, 
		       bool hasp01 /* if has initial model */);
/*< solver constructor >*/


void sp_cconjgrad_close(void);
/*< Free allocated space >*/


void sp_cconjgrad(sp_coperator prec     /* data preconditioning */, 
		  sp_coperator oper     /* linear operator */, 
		  sp_coperator shape    /* shaping operator */, 
		  sp_complex* p         /* preconditioned model */, 
		  sp_complex* x         /* estimated model */, 
		  const sp_complex* dat /* data */, 
		  int niter             /* number of iterations */);
/*< Conjugate gradient solver with shaping >*/



#endif