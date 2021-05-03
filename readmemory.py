import bpy, ctypes
from ctypes import Structure, POINTER


class BezTriple(Structure):
    """
    typedef struct BezTriple {
      float vec[3][3];
      float tilt;
      float weight;
      float radius;
      char ipo;
      char h1, h2;
      char f1, f2, f3;
      char hide;
      char easing;
      float back;
      float amplitude, period;
      char f5;
      char _pad[3];
    } BezTriple;
    """

    _fields_ = [
        ("vec", ctypes.c_float * 3 * 3),

        ("tilt", ctypes.c_float),
        ("weight", ctypes.c_float),
        ("radius", ctypes.c_short),

        ("ipo", ctypes.c_char),

        ("h1", ctypes.c_char),
        ("h2", ctypes.c_char),

        ("f1", ctypes.c_char),
        ("f2", ctypes.c_char),
        ("f3", ctypes.c_char),

        ("hide", ctypes.c_char),

        ("easing", ctypes.c_char),

        ("back", ctypes.c_float),
        ("amplitude", ctypes.c_float),
        ("period", ctypes.c_float),

        ("f5", ctypes.c_char),
        ("_pad", ctypes.c_char * 3),
    ]


class BPoint(Structure):
    """
    typedef struct BPoint {
      float vec[4];
      float tilt;
      float weight;
      short f1, hide;
      float radius;
      char _pad[4];
    } BPoint;
    """
    _fields_ = [
        ("vec", ctypes.c_float * 4),

        ("tilt", ctypes.c_float),
        ("weight", ctypes.c_float),

        ("f1", ctypes.c_short),
        ("hide", ctypes.c_short),

        ("radius", ctypes.c_float),
        ("_pad", ctypes.c_char * 4),
    ]


class Nurb(Structure):
    """
    \source\blender\makesdna\DNA_curve_types.h

    typedef struct Nurb {
      struct Nurb *next, *prev;
      short type;
      short mat_nr;
      short hide, flag;
      int pntsu, pntsv;
      char _pad[4];
      short resolu, resolv;
      short orderu, orderv;
      short flagu, flagv;

      float *knotsu, *knotsv;
      BPoint *bp;
      BezTriple *bezt;

      short tilt_interp;
      short radius_interp;

      int charidx;
    } Nurb;"""

    _fields_ = [
        # ("next", POINTER(Nurb)),
        ("next", ctypes.c_void_p),
        ("prev", ctypes.c_void_p),

        ("type", ctypes.c_short),

        ("mat_nr", ctypes.c_short),
        ("hide", ctypes.c_short),
        ("flag", ctypes.c_short),
        ("pntsu", ctypes.c_int),
        ("pntsv", ctypes.c_int),
        ("_pad", ctypes.c_char_p),

        ("resolu", ctypes.c_short),
        ("resolv", ctypes.c_short),
        ("orderu", ctypes.c_short),
        ("orderv", ctypes.c_short),
        ("flagu", ctypes.c_short),
        ("flagv", ctypes.c_short),
        ("knotsu", POINTER(ctypes.c_float)),
        ("knotsv", POINTER(ctypes.c_float)),

        ("bp", POINTER(BPoint)),
        ("bezt", POINTER(BezTriple)),

        ("tilt_interp", ctypes.c_short),
        ("radius_interp", ctypes.c_short),

        ("charidx", ctypes.c_short),
    ]

spline_ptr = bpy.context.object.data.splines[0].as_pointer()

p = ctypes.POINTER(Nurb)
p.from_address(spline_ptr)

print(p)
print(p.resolu)





#class SocketRef(Structure):
    """
    \source\blender\nodes\NOD_node_tree_ref.hh
    

   class SocketRef : NonCopyable, NonMovable {
 protected:
  NodeRef *node_;
  bNodeSocket *bsocket_;
  bool is_input_;
  int id_;
  int index_;
  PointerRNA rna_;
  Vector<LinkRef *> directly_linked_links_;

  /* These sockets are linked directly, i.e. with a single link in between. */
  MutableSpan<const SocketRef *> directly_linked_sockets_;
  /* These sockets are linked when reroutes, muted links and muted nodes have been taken into
   * account. */
  MutableSpan<const SocketRef *> logically_linked_sockets_;
  /* These are the sockets that have been skipped when searching for logically linked sockets.
   * That includes for example the input and output socket of an intermediate reroute node. */
  MutableSpan<const SocketRef *> logically_linked_skipped_sockets_;"""


"""
typedef struct bNodeSocket {
  struct bNodeSocket *next, *prev, *new_sock;

  /** User-defined properties. */
  IDProperty *prop;

  /** Unique identifier for mapping. */
  char identifier[64];

  /** MAX_NAME. */
  char name[64];

  /* XXX deprecated, only used for the Image and OutputFile nodes,
   * should be removed at some point.
   */
  /** Custom storage. */
  void *storage;

  short type, flag;
  /** Max. number of links. Read via nodeSocketLinkLimit, because the limit might be defined on the
   * socket type. */
  short limit;
  /** Input/output type. */
  short in_out;
  /** Runtime type information. */
  struct bNodeSocketType *typeinfo;
  /** Runtime type identifier. */
  char idname[64];

  float locx, locy;

  /** Default input value used for unlinked sockets. */
  void *default_value;

  /* execution data */
  /** Local stack index. */
  short stack_index;
  /* XXX deprecated, kept for forward compatibility */
  short stack_type DNA_DEPRECATED;
  char display_shape;
  char _pad[1];
  /* Runtime-only cache of the number of input links, for multi-input sockets. */
  short total_inputs;

  /** Custom dynamic defined label, MAX_NAME. */
  char label[64];
  char description[64];

  /** Cached data from execution. */
  void *cache;

  /* internal data to retrieve relations and groups
   * DEPRECATED, now uses the generic identifier string instead
   */
  /** Group socket identifiers, to find matching pairs after reading files. */
  int own_index DNA_DEPRECATED;
  /* XXX deprecated, only used for restoring old group node links */
  int to_index DNA_DEPRECATED;
  /* XXX deprecated, still forward compatible since verification
   * restores pointer from matching own_index. */
  struct bNodeSocket *groupsock DNA_DEPRECATED;

  /** A link pointer, set in ntreeUpdateTree. */
  struct bNodeLink *link;

  /* XXX deprecated, socket input values are stored in default_value now.
   * kept for forward compatibility */
  /** Custom data for inputs, only UI writes in this. */
  bNodeStack ns DNA_DEPRECATED;
} bNodeSocket;
"""

from ctypes import *

class bNodeSocket(Structure):
    pass
   
bNodeSocket._fields_ = [
    ("next", POINTER(bNodeSocket)),
    ("prev", POINTER(bNodeSocket)),
    ("new_sock", POINTER(bNodeSocket)),
    ("prop", c_void_p),
    ("identifier", c_char * 64), # char identifier[64];
    ("name", c_char * 64), # char name[64];
    
    ("storage", c_void_p), # void *storage;
    
    ("type", c_short), # short type, flag; limit in_out
    ("flag", c_short),
    ("limit", c_short),
    ("in_out", c_short),
    
    ("typeinfo", c_void_p), # struct bNodeSocketType *typeinfo;
    ("idname", c_char * 64), # char idname[64];
    
    #float locx, locy;
    ("locx", c_float),
    ("locy", c_float),
    
    #void *default_value;
    ("default_value", c_void_p),
    
    # /* execution data */
    # /** Local stack index. */
    # short stack_index;
    # /* XXX deprecated, kept for forward compatibility */
    # short stack_type DNA_DEPRECATED;
    # char display_shape;
    # char _pad[1];
    # /* Runtime-only cache of the number of input links, for multi-input sockets. */
    # short total_inputs;
    ("stack_index", c_short),
    ("stack_type", c_short),
    ("display_shape", c_char),
    ("_pad", c_char),
    ("total_inputs", c_short),
    
    #/** Custom dynamic defined label, MAX_NAME. */
    #char label[64];
    #char description[64];
    ("label", c_char * 64),
    ("description", c_char * 64),
    
    #/** Cached data from execution. */
    #void *cache;
    #/* internal data to retrieve relations and groups
    #* DEPRECATED, now uses the generic identifier string instead
    #*/
    #/** Group socket identifiers, to find matching pairs after reading files. */
    #int own_index DNA_DEPRECATED;
    #/* XXX deprecated, only used for restoring old group node links */
    #int to_index DNA_DEPRECATED;
    #/* XXX deprecated, still forward compatible since verification
    #* restores pointer from matching own_index. */
    #struct bNodeSocket *groupsock DNA_DEPRECATED;
    #/** A link pointer, set in ntreeUpdateTree. */
    #struct bNodeLink *link;
    
    ("cache", c_void_p),
    ("own_index", c_int),
    ("to_index", c_int),
    ("groupsock", POINTER(bNodeSocket)),
    ("bNodeLink", c_void_p),
]



def show(o):
    for field_name, field_type in o._fields_:
        print(field_name, getattr(o, field_name))

o = bNodeSocket.from_address(tr.inputs[0].as_pointer())
show(o)

class SocketRef(Structure):
    _fields_ = [
        ("node_", c_void_p),
        ("bsocket_", POINTER(bNodeSocket)),
        ("is_input_", c_bool),
        ("id_", c_int),
        ("index_", c_int),
    ]



p = ctypes.POINTER(SocketRef)
o = p.from_address(tr.inputs[0].as_pointer())



"""
typedef struct bNodeType {
  void *next, *prev;

  char idname[64]; /* identifier name */
  int type;

  char ui_name[64]; /* MAX_NAME */
  char ui_description[256];
  int ui_icon;

  float width, minwidth, maxwidth;
  float height, minheight, maxheight;
  short nclass, flag;
"""

class bNodeType(Structure):
    _fields_ = [
        ("next", c_void_p),
        ("prev", c_void_p),
        ("idname", c_char * 64),
        ("type", c_int),
        ("ui_name", c_char * 64),
        ("ui_description", c_char * 256),
        ("ui_icon", c_int),
        ("width", c_float),
        ("minwidth", c_float),
        ("maxwidth", c_float),
        ("height", c_float),
        ("minheight", c_float),
        ("maxheight", c_float),
        ("nclass", c_short),
        ("flag", c_short),
        
    ]


p = ctypes.POINTER(bNodeType)
o = p.from_address(tr.inputs[0].as_pointer())
o = p.from_address(tr.as_pointer())


o = bNodeType.from_address(tr.as_pointer())

o = bNodeType.from_address(bpy.types.GeometryNodeTransform.bl_rna.as_pointer())
for field_name, field_type in o._fields_: print(field_name, getattr(o, field_name))








class bNode(Structure):
    pass
   
bNode._fields_ = [
    # struct bNode *next, *prev, *new_node;
    ("next", POINTER(bNode)),
    ("prev", POINTER(bNode)),
    ("new_node", POINTER(bNode)),
    


    #/** User-defined properties. */
    #IDProperty *prop;
    
    ("prop", c_void_p),
    #
    #/** Runtime type information. */
    #struct bNodeType *typeinfo;
    
    ("typeinfo", POINTER(bNodeType)),
    #/** Runtime type identifier. */
    #char idname[64];
    ("idname", c_char * 64),
    #
    #/** MAX_NAME. */
    #char name[64];
    ("name", c_char * 64),
    #int flag;
    ("flag", c_int),
    #short type;
    ("type", c_short),
    #/** Both for dependency and sorting. */
    #short done, level;
    #
    #/** Used as a boolean for execution. */
    #uint8_t need_exec;
    #
    #char _pad[1];
    #
    #/** Custom user-defined color. */
    #float color[3];
    #
    #ListBase inputs, outputs;
    #/** Parent node. */
    #struct bNode *parent;
    #/** Optional link to libdata. */
    #struct ID *id;
    #/** Custom data, must be struct, for storage in file. */
    #void *storage;
    #/** The original node in the tree (for localized tree). */
    #struct bNode *original;
    #/** List of cached internal links (input to output), for muted nodes and operators. */
    #ListBase internal_links;
    #
    #/** Root offset for drawing (parent space). */
    #float locx, locy;
    #/** Node custom width and height. */
    #float width, height;
    #/** Node width if hidden. */
    #float miniwidth;
    #/** Additional offset from loc. */
    #float offsetx, offsety;
    #/** Initial locx for insert offset animation. */
    #float anim_init_locx;
    #/** Offset that will be added to locx for insert offset animation. */
    #float anim_ofsx;
    #
    #/** Update flags. */
    #int update;
    #
    #/** Custom user-defined label, MAX_NAME. */
    #char label[64];
    #/** To be abused for buttons. */
    #short custom1, custom2;
    #float custom3, custom4;
    #
    #char _pad1[4];
    #
    #/** Entire boundbox (worldspace). */
    #rctf totr;
    #/** Optional buttons area. */
    #rctf butr;
    #/** Optional preview area. */
    #rctf prvr;
    #/**
    #* XXX TODO
    #* Node totr size depends on the prvr size, which in turn is determined from preview size.
    #* In earlier versions bNodePreview was stored directly in nodes, but since now there can be
    #* multiple instances using different preview images it is possible that required node size
    #* varies between instances. preview_xsize, preview_ysize defines a common reserved size for
    #* preview rect for now, could be replaced by more accurate node instance drawing,
    #* but that requires removing totr from DNA and replacing all uses with per-instance data.
    #*/
    #/** Reserved size of the preview rect. */
    #short preview_xsize, preview_ysize;
    #/** Used at runtime when going through the tree. Initialize before use. */
    #short tmp_flag;
    #/** Used at runtime to tag derivatives branches. EEVEE only. */
    #char branch_tag;
    #/** Used at runtime when iterating over node branches. */
    #char iter_flag;
    #/** Runtime during drawing. */
    #struct uiBlock *block;
    #
    #/**
    #* XXX: eevee only, id of screen space reflection layer,
    #* needs to be a float to feed GPU_uniform.
    #*/
    #float ssr_id;
    #/**
    #* XXX: eevee only, id of screen subsurface scatter layer,
    #* needs to be a float to feed GPU_uniform.
    #*/
    #float sss_id;
]
    
o = bNode.from_address(tr.as_pointer())
show(o);