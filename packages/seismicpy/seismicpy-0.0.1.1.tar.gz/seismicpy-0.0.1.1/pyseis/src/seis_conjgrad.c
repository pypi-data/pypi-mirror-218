#include <math.h>
#include <stdio.h>
#include <stdbool.h>
#include "seis_alloc.h"
#include "seis_conjgrad.h"
#include "seis_komplex.h"

#ifndef KISS_FFT_H
#include "seis_kissfft.h"
#endif

static int np, nx, nr, nd;
static sp_complex *r, *d, *sp, *sx, *sr, *gp, *gx, *gr;
static float eps, tol;
static bool verb, hasp0;

void sp_adjnull (bool adj /* adjoint flag */, 
		 bool add /* addition flag */, 
		 int nx   /* size of x */, 
		 int ny   /* size of y */, 
		 float* x, 
		 float* y) 
/*< Zeros out the output (unless add is true). 
  Useful first step for any linear operator. >*/
{
    int i;
    
    if(add) return;
    
    if(adj) {
	for (i = 0; i < nx; i++) {
	    x[i] = 0.;
	}
    } else {
	for (i = 0; i < ny; i++) {
	    y[i] = 0.;
	}
    }
}

void sp_cadjnull (bool adj /* adjoint flag */, 
		  bool add /* addition flag */, 
		  int nx   /* size of x */, 
		  int ny   /* size of y */, 
		  sp_complex* x, 
		  sp_complex* y) 
/*< adjnull version for complex data. >*/
{
    int i;
    
    if(add) return;
    
    if(adj) {
	for (i = 0; i < nx; i++) {
	    x[i] = sp_cmplx(0.0,0.0);
	}
    } else {
	for (i = 0; i < ny; i++) {
	    y[i] = sp_cmplx(0.0,0.0);
	}
    }
}


static double norm (int n, const sp_complex* x) 
/* double-precision L2 norm of a complex number */
{
    double prod, xi, yi;
    int i;

    prod = 0.;
    for (i = 0; i < n; i++) {
	xi = (double) crealf(x[i]);
	yi = (double) cimagf(x[i]);
	prod += xi*xi + yi*yi;
    }
    return prod;
}

void sp_cconjgrad_init(int np1     /* preconditioned size */, 
		       int nx1     /* model size */, 
		       int nd1     /* data size */, 
		       int nr1     /* residual size */, 
		       float eps1  /* scaling */,
		       float tol1  /* tolerance */, 
		       bool verb1  /* verbosity flag */, 
		       bool hasp01 /* if has initial model */) 
/*< solver constructor >*/
{
    np = np1; 
    nx = nx1;
    nr = nr1;
    nd = nd1;
    eps = eps1*eps1;
    tol = tol1;
    verb = verb1;
    hasp0 = hasp01;

    r = sp_complexalloc(nr);  
    d = sp_complexalloc(nd); 
    sp = sp_complexalloc(np);
    gp = sp_complexalloc(np);
    sx = sp_complexalloc(nx);
    gx = sp_complexalloc(nx);
    sr = sp_complexalloc(nr);
    gr = sp_complexalloc(nr);
}

void sp_cconjgrad_close(void) 
/*< Free allocated space >*/
{
    free (r);
    free (d);
    free (sp);
    free (gp);
    free (sx);
    free (gx);
    free (sr);
    free (gr);
}

void sp_cconjgrad(sp_coperator prec     /* data preconditioning */, 
		  sp_coperator oper     /* linear operator */, 
		  sp_coperator shape    /* shaping operator */, 
		  sp_complex* p         /* preconditioned model */, 
		  sp_complex* x         /* estimated model */, 
		  const sp_complex* dat /* data */, 
		  int niter             /* number of iterations */)
/*< Conjugate gradient solver with shaping >*/
{
    double gn, gnp, alpha, beta, g0, dg, r0, b0;
    int i, iter;
    
    if (NULL != prec) {
	for (i=0; i < nd; i++) {
	    d[i] = sp_cneg(dat[i]);
	}
	prec(false,false,nd,nr,d,r);
    } else {
	for (i=0; i < nr; i++) {
	    r[i] = sp_cneg(dat[i]);
	}
    }
    
    if (hasp0) { /* initial p */
	shape(false,false,np,nx,p,x);
	if (NULL != prec) {
	    oper(false,false,nx,nd,x,d);
	    prec(false,true,nd,nr,d,r);
	} else {
	    oper(false,true,nx,nr,x,r);
	}
    } else {
	for (i=0; i < np; i++) {
	    p[i] = sp_cmplx(0.0,0.0);
	}
	for (i=0; i < nx; i++) {
	    x[i] = sp_cmplx(0.0,0.0);
	}
    } 
    
    dg = g0 = b0 = gnp = 0.;
    r0 = verb? norm(nr,r): 0.;

    for (iter=0; iter < niter; iter++) {
	for (i=0; i < np; i++) {
	    gp[i] = sp_crmul(p[i],eps);
	}
	for (i=0; i < nx; i++) {
	    gx[i] = sp_crmul(x[i],-eps);
	}

	if (NULL != prec) {
	    prec(true,false,nd,nr,d,r);
	    oper(true,true,nx,nd,gx,d);
	} else {
	    oper(true,true,nx,nr,gx,r);
	}

	shape(true,true,np,nx,gp,gx);
	shape(false,false,np,nx,gp,gx);

	if (NULL != prec) {
	    oper(false,false,nx,nd,gx,d);
	    prec(false,false,nd,nr,d,gr);
	} else {
	    oper(false,false,nx,nr,gx,gr);
	}

	gn = norm(np,gp);

	if (iter==0) {
	    g0 = gn;
	    b0 = fabs(gn + eps*(norm(nr,gr)-norm(nx,gx)));

	    for (i=0; i < np; i++) {
		sp[i] = gp[i];
	    }
	    for (i=0; i < nx; i++) {
		sx[i] = gx[i];
	    }
	    for (i=0; i < nr; i++) {
		sr[i] = gr[i];
	    }
	} else {
	    alpha = gn / gnp;
	    dg = gn / g0;

	    if (alpha < tol || dg < tol) {
		if (verb) 
		    printf(
			"convergence in %d iterations, alpha=%g, gd=%g\n",
			iter,alpha,dg);
		break;
	    }

	    for (i=0; i < np; i++) {
		sp[i] = sp_cadd(gp[i],sp_crmul(sp[i],alpha));
	    }
	    for (i=0; i < nx; i++) {
		sx[i] = sp_cadd(gx[i],sp_crmul(sx[i],alpha));
	    }
	    for (i=0; i < nr; i++) {
		sr[i] = sp_cadd(gr[i],sp_crmul(sr[i],alpha));
	    }
	}

	beta = norm(nr,sr) + eps*(norm(np,sp) - norm(nx,sx));

	/*
	if (beta/b0 < tol) {
	    if (verb) 
		printf("convergence in %d iterations, beta=%g",iter,beta);
	    break;
	}
	*/
	
	if (verb) printf("iteration %d res: %f grad: %f\n",
			     iter,norm(nr,r)/r0,dg);

	alpha = - gn / beta;

	for (i=0; i < np; i++) {
	    p[i] = sp_cadd(p[i],sp_crmul(sp[i],alpha));
	}

	for (i=0; i < nx; i++) {
	    x[i] = sp_cadd(x[i],sp_crmul(sx[i],alpha));
	}

	for (i=0; i < nr; i++) {
	    r[i] = sp_cadd(r[i],sp_crmul(sr[i],alpha));
	}

	gnp = gn;
    }
}
