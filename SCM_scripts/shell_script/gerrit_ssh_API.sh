#!/bin/bash
ssh -p 29418 10.0.30.9 gerrit query branch:PDU3_DEV after:2018-04-09  project:^MSM89XX_O_CODE_SW3/.*  status:merged
