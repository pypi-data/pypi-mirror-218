/* Triangle smoothing for complex numbers */

// #include "ctriangle.h"
// #include "alloc.h"
// 
// #include "_bool.h"
// #include "komplex.h"
/*^*/
#include <stdbool.h>
#include "seis_dtype.h"
#include "seis_komplex.h"
#include "seis_alloc.h"
#include "seis_triangle.h"


static void fold (int o, int d, int nx, int nb, int np, 
		 sp_complex *x, const sp_complex* tmp);
static void doubint (int nx, sp_complex *x, bool der);
static void triple (int o, int d, int nx, int nb, const sp_complex* x, sp_complex* tmp, bool box, float wt);

sp_ctriangle sp_ctriangle_init (int nbox /* triangle length */, 
				int ndat /* data length */,
				bool box /* if box instead of triangle */)
/*< initialize >*/
{
    sp_ctriangle tr;

    tr = (sp_ctriangle) sp_alloc(1,sizeof(*tr));

    tr->nx = ndat;
    tr->nb = nbox;
    tr->box = box;
    tr->np = ndat + 2*nbox;

    if (box) {
	tr->wt = 1.0/(2*nbox-1);
    } else {
	tr->wt = 1.0/(nbox*nbox);
    }
    
    tr->tmp = sp_complexalloc(tr->np);

    return tr;
}

static void fold (int o, int d, int nx, int nb, int np, 
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
    
static void doubint (int nx, sp_complex *xx, bool der)
{
    int i;
    sp_complex t;


    /* integrate forward */
    t=sp_cmplx(0.,0.);
    for (i=0; i < nx; i++) {
	t = sp_cadd(t,xx[i]);
	xx[i] = t;
    }

    if (der) return;

    /* integrate backward */
    t = sp_cmplx(0.,0.);
    for (i=nx-1; i >= 0; i--) {
	t = sp_cadd(t,xx[i]);
	xx[i] = t;
    }
}

static void triple (int o, int d, int nx, int nb, const sp_complex* x, sp_complex* tmp, bool box, float wt)
{
    int i;
    sp_complex xi;

    for (i=0; i < nx + 2*nb; i++) {
	tmp[i] = sp_cmplx(0.,0.);
    }

    if (box) {
	for (i=0; i < nx; i++) {
	    xi = sp_crmul(x[o+i*d],wt);

	    tmp[i+1]    = sp_cadd(tmp[i+1],xi);
	    tmp[i+2*nb] = sp_cadd(tmp[i+2*nb],sp_cneg(xi));
	}
    } else {
	for (i=0; i < nx; i++) {
	    xi = sp_crmul(x[o+i*d],wt);

	    tmp[i]      = sp_cadd(tmp[i],sp_cneg(xi));
	    tmp[i+nb]   = sp_cadd(tmp[i+nb],sp_crmul(xi,2.));
	    tmp[i+2*nb] = sp_cadd(tmp[i+2*nb],sp_cneg(xi));
	}
    }
}

void sp_csmooth (sp_ctriangle tr    /* smoothing object */, 
		 int o, int d    /* trace sampling */, 
		 bool der        /* if derivative */,
		 sp_complex *x   /* data (smoothed in place) */)
/*< apply adjoint triangle smoothing >*/
{
    triple (o,d,tr->nx,tr->nb,x,tr->tmp,tr->box,tr->wt);
    doubint (tr->np,tr->tmp,(bool) (tr->box || der));
    fold (o,d,tr->nx,tr->nb,tr->np,x,tr->tmp);
}

void  sp_ctriangle_close(sp_ctriangle tr)
/*< free allocated storage >*/
{
    free (tr->tmp);
    free (tr);
}




