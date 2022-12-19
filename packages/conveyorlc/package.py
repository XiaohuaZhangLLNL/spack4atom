##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install example
#
# You can edit this file again by typing:
#
#     spack edit example
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import os


class Conveyorlc(CMakePackage):
    """
    A Parallel Virtual Screening Pipeline for Docking and MM/GSBA.
    """

    homepage = "https://github.com/XiaohuaZhangLLNL/conveyorlc"
    url = (
        "https://github.com/XiaohuaZhangLLNL/conveyorlc/archive/refs/tags/v1.1.2.tar.gz"
    )
    git = "https://github.com/XiaohuaZhangLLNL/conveyorlc.git"

    version("master", branch="master")

    depends_on("boost+mpi")
    depends_on("conduit@0.8.4 +hdf5")
    depends_on("h5cpp")
    depends_on("hdf5")
    depends_on("openbabel@3.0.0 ~python ~gui")
    depends_on("sqlite")
    # depends_on('mpi')

    depends_on("cmake", type="build")

    def patch(self):
        """
        Patch to remove conduit - we can define these on our own.
        """
        with working_dir(self.stage.source_path):
            os.remove(os.path.join("cmake", "FindConduit.cmake"))

    def cmake_args(self):
        args = [
            "-DOPENBABEL3_INCLUDE_DIRS=%s"
            % os.path.join(self.spec["openbabel"].prefix, "include", "openbabel3"),
            "-DCONDUIT_DIR=%s" % self.spec["conduit"].prefix,
            "-DCONDUIT_FOUND=TRUE",
            "-DH5CPP_INCLUDE_DIRS=%s"
            % os.path.join(self.spec["h5cpp"].prefix, "include"),
            "-DCONDUIT_INCLUDE_DIRS=%s"
            % os.path.join(self.spec["conduit"].prefix, "include", "conduit"),
            "-DCMAKE_CXX_FLAGS=-lhdf5",
            "-DHDF5_ROOT=%s" % self.spec["hdf5"].prefix,
            "-DHDF5_LIBRARIES=%s" % os.path.join(self.spec["hdf5"].prefix, "lib"),
            "-DHDF5_INCLUDE_DIRS=%s"
            % os.path.join(self.spec["hdf5"].prefix, "include"),
        ]
        return args
