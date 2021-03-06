# ----------------------------------------------------------------------------
# PyWavefront
# Copyright (c) 2013 Kurt Yoder
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

from pyglet.gl import *

import parser
import texture

class Material(object):
    # set defaults
    diffuse = [.8, .8, .8]
    ambient = [.2, .2, .2]
    specular = [0., 0., 0.]
    emission = [0., 0., 0.]
    shininess = 0.
    opacity = 1.
    texture = None

    def __init__(self, name):
        self.name = name

        # Interleaved array of floats in GL_T2F_N3F_V3F format
        self.vertices = []
        self.gl_floats = None

    def set_texture(self, path):
        self.texture = texture.Texture(path)

    def gl_light(self, lighting):
        """Return a GLfloat with length 4, containing the 3 lighting values and
        appending opacity."""
        return (GLfloat * 4)(*(lighting + [self.opacity]))

    def draw(self, face=GL_FRONT_AND_BACK):
        if self.texture:
            self.texture.draw()
        else:
            glDisable(GL_TEXTURE_2D)

        glMaterialfv(face, GL_DIFFUSE, self.gl_light(self.diffuse) )
        glMaterialfv(face, GL_AMBIENT, self.gl_light(self.ambient) )
        glMaterialfv(face, GL_SPECULAR, self.gl_light(self.specular) )
        glMaterialfv(face, GL_EMISSION, self.gl_light(self.emission) )
        glMaterialf(face, GL_SHININESS, self.shininess)

        if self.gl_floats is None:
            self.gl_floats = (GLfloat * len(self.vertices))(*self.vertices)
            self.triangle_count = len(self.vertices) / 8
        glInterleavedArrays(GL_T2F_N3F_V3F, 0, self.gl_floats)
        glDrawArrays(GL_TRIANGLES, 0, self.triangle_count)

class MaterialParser(parser.Parser):
    """Object to parse lines of a materials definition file."""

    def __init__(self, file_path):
        self.materials = {}
        self.this_material = None
        self.read_file(file_path)

    def parse_newmtl(self, args):
        [newmtl] = args
        self.this_material = Material(newmtl)
        self.materials[self.this_material.name] = self.this_material

    def parse_Kd(self, args):
        self.this_material.diffuse = map(float, args[0:])

    def parse_Ka(self, args):
        self.this_material.ambient = map(float, args[0:])

    def parse_Ks(self, args):
        self.this_material.specular = map(float, args[0:])

    def parse_Ke(self, args):
        self.this_material.emissive = map(float, args[0:])

    def parse_Ns(self, args):
        [Ns] = args
        self.this_material.shininess = float(Ns)

    def parse_d(self, args):
        [d] = args
        self.this_material.opacity = float(d)

    def parse_map_Kd(self, args):
        [Kd] = args
        self.this_material.set_texture(Kd)

    def parse_Ni(self, args):
        # don't know what this does
        return

    def parse_illum(self, args):
        # don't know what this does
        return
