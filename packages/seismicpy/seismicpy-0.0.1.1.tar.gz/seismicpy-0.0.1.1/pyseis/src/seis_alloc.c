#include <stdlib.h>
#include <stdio.h>
// #include <complex.h>

#include "seis_alloc.h"

void *sp_alloc (size_t n    /* number of elements */, 
			  size_t size /* size of one element */)
/*< output-checking allocation >*/
{
    void *ptr; 
    
    size *= n;
    
    ptr = malloc (size);

    if (NULL == ptr)
	{
	printf("cannot allocate %lu bytes:", size);
	return NULL;
	}

    return ptr;
}

float *sp_floatalloc (size_t n /* number of elements */)
	  /*< float allocation >*/ 
{
    float *ptr;
    ptr = (float*) sp_alloc (n,sizeof(float));
    return ptr;
}

float **sp_floatalloc2 (size_t n1 /* fast dimension */, 
				  size_t n2 /* slow dimension */)
/*< float 2-D allocation, out[0] points to a contiguous array >*/ 
{
    size_t i2;
    float **ptr;
    
    ptr = (float**) sp_alloc (n2,sizeof(float*));
    ptr[0] = sp_floatalloc (n1*n2);
    for (i2=1; i2 < n2; i2++) {
	ptr[i2] = ptr[0]+i2*n1;
    }
    return ptr;
}

float ***sp_floatalloc3 (size_t n1 /* fast dimension */, 
				   size_t n2 /* slower dimension */, 
				   size_t n3 /* slowest dimension */)
/*< float 3-D allocation, out[0][0] points to a contiguous array >*/ 
{
    size_t i3;
    float ***ptr;
    
    ptr = (float***) sp_alloc (n3,sizeof(float**));
    ptr[0] = sp_floatalloc2 (n1,n2*n3);
    for (i3=1; i3 < n3; i3++) {
	ptr[i3] = ptr[0]+i3*n2;
    }
    return ptr;
}

int *sp_intalloc (size_t n /* number of elements */)
	  /*< int allocation >*/  
{
    int *ptr;
    ptr = (int*) sp_alloc (n,sizeof(int));
    return ptr;
}

int **sp_intalloc2 (size_t n1 /* fast dimension */, 
			      size_t n2 /* slow dimension */)
/*< float 2-D allocation, out[0] points to a contiguous array >*/  
{
    size_t i2;
    int **ptr;
    
    ptr = (int**) sp_alloc (n2,sizeof(int*));
    ptr[0] = sp_intalloc (n1*n2);
    for (i2=1; i2 < n2; i2++) {
	ptr[i2] = ptr[0]+i2*n1;
    }
    return ptr;
}

int ***sp_intalloc3 (size_t n1 /* fast dimension */, 
			       size_t n2 /* slower dimension */, 
			       size_t n3 /* slowest dimension */)
/*< int 3-D allocation, out[0][0] points to a contiguous array >*/ 
{
    size_t i3;
    int ***ptr;
    
    ptr = (int***) sp_alloc (n3,sizeof(int**));
    ptr[0] = sp_intalloc2 (n1,n2*n3);
    for (i3=1; i3 < n3; i3++) {
	ptr[i3] = ptr[0]+i3*n2;
    }
    return ptr;
}

sp_complex *sp_complexalloc (size_t n /* number of elements */) 
	  /*< complex allocation >*/
{
    sp_complex *ptr;
    ptr = (sp_complex*) sp_alloc (n,sizeof(sp_complex));
    return ptr;
}

sp_complex **sp_complexalloc2 (size_t n1 /* fast dimension */, 
					 size_t n2 /* slow dimension */)
	  /*< complex 2-D allocation >*/ 
{
    size_t i2;
    sp_complex **ptr;
    
    ptr = (sp_complex**) sp_alloc (n2,sizeof(sp_complex*));
    ptr[0] = sp_complexalloc (n1*n2);
    for (i2=1; i2 < n2; i2++) {
	ptr[i2] = ptr[0]+i2*n1;
    }
    return ptr;
}

sp_complex ***sp_complexalloc3 (size_t n1 /* fast dimension */, 
					  size_t n2 /* slower dimension */, 
					  size_t n3 /* slowest dimension */)
	  /*< complex 3-D allocation >*/ 
{
    size_t i3;
    sp_complex ***ptr;
    
    ptr = (sp_complex***) sp_alloc (n3,sizeof(sp_complex**));
    ptr[0] = sp_complexalloc2 (n1,n2*n3);
    for (i3=1; i3 < n3; i3++) {
	ptr[i3] = ptr[0]+i3*n2;
    }
    return ptr;
}


