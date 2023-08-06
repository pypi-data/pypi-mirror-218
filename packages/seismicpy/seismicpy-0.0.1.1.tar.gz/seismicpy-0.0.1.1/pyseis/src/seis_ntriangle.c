/* Non-stationary triangle smoothing (fixed version) 
Note Fomel's ntriangle.c may contain bugs in user/fomel/ntriangle.c
t[i] -> t[o+i*d]; s[i]->s[o+i*d] in triple 
for both real (future?) and complex values
*/

// #include <rsf.h>

#include <stdbool.h>
#include "seis_dtype.h"
#include "seis_komplex.h"
#include "seis_alloc.h"
#include "seis_triangle.h"
#include "seis_ntriangle.h"

// #ifndef ntriangle_h
// 
// typedef struct CNtriangle *cntriangle;
// /* abstract data type */
// /*^*/
// 
// #endif

// struct CNtriangle {
//     sp_complex *tmp;
//     int np, nb, nx;
// };
// 
// typedef struct CNtriangle *cntriangle;
// /* abstract data type */

static void cfold (int o, int d, int nx, int nb, int np, 
		  const sp_complex *x, sp_complex* tmp);
static void cfold2 (int o, int d, int nx, int nb, int np, 
		   sp_complex *x, const sp_complex* tmp);
static void cdoubint (int nx, sp_complex *x, bool der);
static void ctriple (int o, int d, int nx, int nb, 
		    const float* t, const int* s, sp_complex* x, const sp_complex* tmp);
static void ctriple2 (int o, int d, int nx, int nb, 
		     const float* t, const int* s, const sp_complex* x, sp_complex* tmp);

cntriangle cntriangle_init (int nbox /* maximum triangle length */, 
			  int ndat /* data length */)
/*< initialize >*/
{
    cntriangle tr;

    tr = (cntriangle) sp_alloc(1,sizeof(*tr));

    tr->nx = ndat;
    tr->nb = nbox;
    tr->np = ndat + 2*nbox;
    
    tr->tmp = sp_complexalloc(tr->np);

    return tr;
}

static void cfold (int o, int d, int nx, int nb, int np, 
		  const sp_complex *x, sp_complex* tmp)
{
    int i, j;

    /* copy middle */
    for (i=0; i < nx; i++) 
	tmp[i+nb] = x[o+i*d];
    
    /* reflections from the right side */
    for (j=nb+nx; j < np; j += nx) {
	for (i=0; i < nx && i < np-j; i++)
	    tmp[j+i] = x[o+(nx-1-i)*d];
	j += nx;
	for (i=0; i < nx && i < np-j; i++)
	    tmp[j+i] = x[o+i*d];
    }
    
    /* reflections from the left side */
    for (j=nb; j >= 0; j -= nx) {
	for (i=0; i < nx && i < j; i++)
	    tmp[j-1-i] = x[o+i*d];
	j -= nx;
	for (i=0; i < nx && i < j; i++)
	    tmp[j-1-i] = x[o+(nx-1-i)*d];
    }
}




static void cfold2 (int o, int d, int nx, int nb, int np, 
		   sp_complex *x, const sp_complex* tmp)
{
    int i, j;

    /* copy middle */
    for (i=0; i < nx; i++) 
	x[o+i*d] = tmp[i+nb];

    /* reflections from the right side */
    for (j=nb+nx; j < np; j += nx) {
	for (i=0; i < nx && i < np-j; i++) {
	    x[o+(nx-1-i)*d] = sp_cadd(x[o+(nx-1-i)*d],tmp[j+i]);
	}
	j += nx;
	for (i=0; i < nx && i < np-j; i++) {
	    x[o+i*d] = sp_cadd(x[o+i*d],tmp[j+i]);
	}
    }
    
    /* reflections from the left side */
    for (j=nb; j >= 0; j -= nx) {
	for (i=0; i < nx && i < j; i++) {
	    x[o+i*d] = sp_cadd(x[o+i*d],tmp[j-1-i]);
	}
	j -= nx;
	for (i=0; i < nx && i < j; i++) {
	    x[o+(nx-1-i)*d] = sp_cadd(x[o+(nx-1-i)*d],tmp[j-1-i]);
	}
    }
    
}
    
static void cdoubint (int nx, sp_complex *xx, bool der)
{
    int i;
    sp_complex t;

    /* integrate backward */
    t = sp_cmplx(0.,0.);
    for (i=nx-1; i >= 0; i--) {
	t = sp_cadd(t,xx[i]);

	xx[i] = t;
    }

    if (der) return;

    /* integrate forward */
    t=sp_cmplx(0.,0.);
    for (i=0; i < nx; i++) {
	t = sp_cadd(t,xx[i]);

	xx[i] = t;
    }
}

static void ctriple (int o, int d, int nx, int nb, 
		    const float* t,
		    const int* s,
		    sp_complex* x, const sp_complex* tmp)
{
    int i, nt, nt1, ns;
    float tt, wt, wt1;

    for (i=0; i < nx; i++) {
	tt = t[o+i*d];
	nt = floorf(tt);
	nt1 = nt+1;
	ns = nb + s[o+i*d];
	wt  = (nt1*nt1-tt*tt)/(nt*nt*(nt+nt1));
	wt1 = (tt*tt-nt*nt)/(nt1*nt1*(nt+nt1));

	x[o+i*d] = 	sp_cadd(sp_cadd(sp_crmul(tmp[i+ns],2*(wt+wt1)), sp_cneg(sp_crmul(sp_cadd(tmp[i+ns-nt1],tmp[i+ns+nt1]),wt1))), sp_cneg(sp_crmul(sp_cadd(tmp[i+ns-nt],tmp[i+ns+nt]),wt)));
    }
}

static void ctriple2 (int o, int d, int nx, int nb, 
		     const float* t,
		     const int* s,
		     const sp_complex* x, sp_complex* tmp)
{
    int i, nt, nt1, ns;
	float tt;//, wt, wt1;
	sp_complex wt,wt1;

    for (i=0; i < nx + 2*nb; i++) {
	tmp[i] = sp_cmplx(0.,0.);
    }

    for (i=0; i < nx; i++) {
	tt = t[i];
	nt = floorf(tt);
	nt1 = nt+1;
	ns = nb + s[i];
	wt=sp_crmul(x[o+i*d],(nt1*nt1-tt*tt)/(nt*nt*(nt+nt1)));
	wt1=sp_crmul(x[o+i*d],(tt*tt-nt*nt)/(nt1*nt1*(nt+nt1)));
	tmp[i+ns-nt1] = sp_cadd(tmp[i+ns-nt1],sp_cneg(wt1));
	tmp[i+ns-nt] = sp_cadd(tmp[i+ns-nt],sp_cneg(wt));
	tmp[i+ns] = sp_cadd(tmp[i+ns],sp_crmul(sp_cadd(wt,wt1),2));
	tmp[i+ns+nt] = sp_cadd(tmp[i+ns+nt],sp_cneg(wt));
	tmp[i+ns+nt1] = sp_cadd(tmp[i+ns+nt1],sp_cneg(wt1));
    }
}

void cnsmooth (cntriangle tr /* smoothing object */, 
	      int o, int d /* sampling. o: starting index, d: stride in samples for 1/2/3rd dimension; all refer to a correct index in a 1D vector  */, 
	      bool der     /* derivative flag */, 
	      const float *t /* triangle lengths */, 
	      const int *s /* triangle shifts */,
	      sp_complex *x     /* data (smoothed in place) */)
/*< smooth >*/
{
    cfold (o,d,tr->nx,tr->nb,tr->np,x,tr->tmp); 
    cdoubint (tr->np,tr->tmp,der);
    ctriple (o,d,tr->nx,tr->nb,t,s,x,tr->tmp);
}

void cnsmooth2 (cntriangle tr /* smoothing object */, 
	       int o, int d /* sampling */, 
	       bool der     /* derivative flag */, 
	       const float *t /* triangle lengths */,
	       const int *s /* triangle shifts */,
	       sp_complex *x     /* data (smoothed in place) */)
/*< alternative smooth >*/
{
    ctriple2 (o,d,tr->nx,tr->nb,t,s,x,tr->tmp);
    cdoubint (tr->np,tr->tmp,der);
    cfold2 (o,d,tr->nx,tr->nb,tr->np,x,tr->tmp);
}

void  cntriangle_close(cntriangle tr)
/*< free allocated storage >*/
{
    free (tr->tmp);
    free (tr);
}

