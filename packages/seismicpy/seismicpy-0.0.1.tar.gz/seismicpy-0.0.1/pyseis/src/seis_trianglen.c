/* N-D triangle smoothing as a linear operator for complex numbers */

// #include "ctrianglen.h"
// #include "ctriangle.h"
// #include "alloc.h"
// #include "file.h"
// #include "error.h"
// #include "adjnull.h"
// #include "decart.h"
// 
// #include "_bool.h"
// #include "komplex.h"
/*^*/

#include "seis_conjgrad.h"
#include "seis_komplex.h"
#include "seis_alloc.h"
#include "seis_dtype.h"
#include "seis_triangle.h"
#include "seis_trianglen.h"
#include "seis_decart.h"


#define SF_MAX_DIM 9

static int *n, s[SF_MAX_DIM], nd, dim;
static sp_ctriangle *tr;
static sp_complex *tmp;

void sp_ctrianglen_init (int ndim  /* number of dimensions */, 
			int *nbox /* triangle radius [ndim] */, 
			int *ndat /* data dimensions [ndim] */)
/*< initialize >*/
{
    int i;

    dim = ndim;
    n = sp_intalloc(dim);

    tr = (sp_ctriangle*) sp_alloc(dim,sizeof(sp_ctriangle));

    nd = 1;
    for (i=0; i < dim; i++) {
	tr[i] = (nbox[i] > 1)? sp_ctriangle_init (nbox[i],ndat[i],false): NULL;
	s[i] = nd;
	n[i] = ndat[i];
	nd *= ndat[i];
    }
    tmp = sp_complexalloc (nd);
}

void sp_ctrianglen_lop (bool adj, bool add, int nx, int ny, sp_complex* x, sp_complex* y)
/*< linear operator >*/
{
    int i, j, i0;

//     if (nx != ny || nx != nd) 
// 	sp_error("%s: Wrong data dimensions: nx=%d, ny=%d, nd=%d",
// 		 __FILE__,nx,ny,nd);

    sp_cadjnull (adj,add,nx,ny,x,y);
  
    if (adj) {
	for (i=0; i < nd; i++) {
	    tmp[i] = y[i];
	}
    } else {
	for (i=0; i < nd; i++) {
	    tmp[i] = x[i];
	}
    }

  
    for (i=0; i < dim; i++) {
	if (NULL != tr[i]) {
	    for (j=0; j < nd/n[i]; j++) {
		i0 = sp_first_index (i,j,dim,n,s);
		sp_csmooth (tr[i], i0, s[i], false, tmp);
	    }
	}
    }
	
    if (adj) {
	for (i=0; i < nd; i++) {
	    x[i] = sp_cadd(x[i],tmp[i]);
	}
    } else {
	for (i=0; i < nd; i++) {
	    y[i] = sp_cadd(y[i],tmp[i]);
	}
    }    
}

void sp_ctrianglen_close(void)
/*< free allocated storage >*/
{
    int i;

    free (tmp);

    for (i=0; i < dim; i++) {
	if (NULL != tr[i]) sp_ctriangle_close (tr[i]);
    }

    free(tr);
    free(n);
}

