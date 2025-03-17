#include "foot-features.h"
#include "version.h"

const char version_and_features[] =
    "version: " FOOT_VERSION

#if defined(FOOT_PGO_ENABLED) && FOOT_PGO_ENABLED
    " +pgo"
#else
    " -pgo"
#endif

#if defined(FOOT_IME_ENABLED) && FOOT_IME_ENABLED
    " +ime"
#else
    " -ime"
#endif

#if defined(FOOT_GRAPHEME_CLUSTERING) && FOOT_GRAPHEME_CLUSTERING
    " +graphemes"
#else
    " -graphemes"
#endif

#if !defined(NDEBUG)
    " +assertions"
#else
    " -assertions"
#endif
;
