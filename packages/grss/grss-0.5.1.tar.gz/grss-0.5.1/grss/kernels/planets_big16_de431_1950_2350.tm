\begintext
   
    Custom meta-kernel that loads de431 planetary and big16 asteroid perturber
    ephemerides and latest leapseconds kernel.

    The path_values variable is written by the update_kernels.py script.

\begindata

    PATH_VALUES  = ( '/Users/runner/work/grss/grss/grss/kernel',
                     's' )

    PATH_SYMBOLS = ( 'GRSS1',
                     'GRSS2' )

    KERNELS_TO_LOAD = ( '$GRSS1$GRSS2/latest_leapseconds.tls',
                        '$GRSS1$GRSS2/planets_big16_de431_1950_2350.bsp',
                        '$GRSS1$GRSS2/earth_200101_990825_predict.bpc',
                        '$GRSS1$GRSS2/earth_720101_230601.bpc',
                        '$GRSS1$GRSS2/earth_latest_high_prec.bpc' )

\begintext
