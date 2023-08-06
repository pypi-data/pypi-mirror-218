
#ifndef DTYPE_H
#define DTYPE_H

#ifndef KISS_FFT_H
#include "seis_kissfft.h"
#endif

typedef struct {
    double r, i;
} sp_double_complex;

typedef kiss_fft_cpx sp_complex;


#endif



