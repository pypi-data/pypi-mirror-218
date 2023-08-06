# Copyright (c) 2022, Bamboooz
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from display.arch.windows import display


# Use functions from display.c
screen_resolution = display.get_screen_resolution()
refresh_rate = display.get_refresh_rate()

print("Screen Resolution:", screen_resolution)
print("Refresh Rate:", refresh_rate)
