#!/usr/bin/env python

n_stripes = 10195271

n_colors = 19

# Let a be AAAAA converted from base 36 to base 10

#  x mod 72002149 - 38722868 = a

# Let x be the number of cyclic flags on 10195271 stripes with 19 colors.

# A cyclic flag with n stripes on c colors is a
# configuration of n colored stripes, with c possible colors,
# arranged in a cyclic pattern.
# Rotating or reflecting a cyclic flag yields the same flag.

# number of combinations of 19 colors on 10195271 stripes
# that the order is indifferent as a whole, you can start from any color

# I understand that it's just the number of combinations of 19 colors on 10195271 stripes
# uniquely
import math

x = n_stripes * math.factorial(n_colors)
print("x: " + str(x))

pre_a = x % (72002149 - 38722868)
print("pre_a:" + str(pre_a))
pre_a2 = x % 72002149 - 38722868

# convert from base 10 to base 36
import numpy as np

print("AAAAA is:")
print np.base_repr(pre_a, 36)

print("Or... unprobably: ")
print np.base_repr(pre_a2, 36)

