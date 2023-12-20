.. _`json`:

===================
JSON representation
===================

MID JSON representation
=======================

A full example of a simple MID SB serialised to JSON is given below. This SBDefinition,
identified as 'sbi-mvp01-20200325-00001', defines two field configurations
identified as 'science field' and 'calibrator field' respectively. Field
configuration 'science field' contains 2 sidereal targets, identified as
beam #1 and beam #2 which point at two sidereal positions. Field
configuration 'calibrator field' contains one target with ID 'bandpass
calibrator' which points at Mars. Two scan definitions are defined: a scan
identified as *calibrator scan*, which would observe the field *calibrator field* (=Mars)
for 10 seconds, and a scan identified as *science scan*, which would observe the field
*science field* (=beam #1 and beam #2) for 60 seconds. The scan_sequence says
to observe *calibrator scan*, *science scan*, *science scan*, *calibrator scan*,
so the final observing sequence would be:

#. Observe Mars for 10 seconds
#. Observe beam #1 and beam #2 for 60 seconds
#. Observe beam #1 and beam #2 again for 60 seconds
#. Observe Mars for 10 seconds

SBDefinition also allows to optionally include SDP and CSP configurations.

.. literalinclude:: ../../tests/unit/ska_oso_pdm/schema/common/testfile_sample_mid_sb.json
    :language: JSON



LOW JSON representation
=======================

A full example of a simple SKA LOW SB serialised to JSON is given below.
This LOW SBDefinition, identified as "sbi-mvp01-20200325-00001", defines
a MCCS subarray beam, *beam A*, composed of stations 1 and 2, configured
to output on one channel block. One field consisting of two targets is
defined. The targets are drift scan targets, at 45 degree and 85 degree
elevation respectively. One subarray beam configuration is defined. If
other scans required different subarray beam configurations, they would
be defined here too. The SB then defines two target beam configurations
that link subarray beam configurations to targets: each configuration
points beam A at 45 degree elevation and 85 degree elevation targets
respectively. Two scan definitions are defined that each perform a drift
scan. The first is defined as the 'calibrator scan' that is using the
subarray beam configuration for the first 'target' at 45 degrees
elevation, the second is the 'science scan' which uses the same subarray
beam configuration with the second target at 85 degrees. Finally, the
scan sequence declares the observation to consist of four scans, with a
calibrator scan bookending two science scans performed back-to-back.


.. literalinclude:: ../../tests/unit/ska_oso_pdm/schema/common/testfile_sample_low_sb.json
    :language: JSON
