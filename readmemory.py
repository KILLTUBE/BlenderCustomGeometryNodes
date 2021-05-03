#import bpy, ctypes
from ctypes import *


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

"""
spline_ptr = bpy.context.object.data.splines[0].as_pointer()
p = ctypes.POINTER(Nurb)
p.from_address(spline_ptr)

print(p)
print(p.resolu)
"""




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


class SocketRef(Structure):
    _fields_ = [
        ("node_", c_void_p),
        ("bsocket_", POINTER(bNodeSocket)),
        ("is_input_", c_bool),
        ("id_", c_int),
        ("index_", c_int),
    ]



#p = ctypes.POINTER(SocketRef)
#o = p.from_address(tr.inputs[0].as_pointer())



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


        #/* templates for static sockets */
        #bNodeSocketTemplate *inputs, *outputs;
        ("inputs", c_void_p),
        ("outputs", c_void_p),
        
        #
        #char storagename[64]; /* struct name for DNA */
        ("storagename", c_char * 64),
        #
        #/* Main draw function for the node */
        #void (*draw_nodetype)(const struct bContext *C,
        #                    struct ARegion *region,
        #                    struct SpaceNode *snode,
        #                    struct bNodeTree *ntree,
        #                    struct bNode *node,
        #                    bNodeInstanceKey key);
        ("draw_nodetype", c_void_p),
        #/* Updates the node geometry attributes according to internal state before actual drawing */
        #void (*draw_nodetype_prepare)(const struct bContext *C,
        #                            struct bNodeTree *ntree,
        #                            struct bNode *node);
        ("draw_nodetype_prepare", c_void_p),
        #/* Draw the option buttons on the node */
        #void (*draw_buttons)(struct uiLayout *, struct bContext *C, struct PointerRNA *ptr);
        ("draw_buttons", c_void_p),
        #/* Additional parameters in the side panel */
        #void (*draw_buttons_ex)(struct uiLayout *, struct bContext *C, struct PointerRNA *ptr);
        ("draw_buttons_ex", c_void_p),
        #
        #/* Additional drawing on backdrop */
        #void (*draw_backdrop)(
        #  struct SpaceNode *snode, struct ImBuf *backdrop, struct bNode *node, int x, int y);
        ("draw_backdrop", c_void_p),
        #/**
        #* Optional custom label function for the node header.
        #* \note Used as a fallback when #bNode.label isn't set.
        #*/
        #void (*labelfunc)(struct bNodeTree *ntree, struct bNode *node, char *label, int maxlen);
        ("labelfunc", c_void_p),
        #/** Optional custom resize handle polling. */
        #int (*resize_area_func)(struct bNode *node, int x, int y);
        ("resize_area_func", c_void_p),
        #/** Optional selection area polling. */
        #int (*select_area_func)(struct bNode *node, int x, int y);
        ("select_area_func", c_void_p),
        #/** Optional tweak area polling (for grabbing). */
        #int (*tweak_area_func)(struct bNode *node, int x, int y);
        ("tweak_area_func", c_void_p),
        #
        #/** Called when the node is updated in the editor. */
        #void (*updatefunc)(struct bNodeTree *ntree, struct bNode *node);
        ("updatefunc", c_void_p),
        #/** Check and update if internal ID data has changed. */
        #void (*group_update_func)(struct bNodeTree *ntree, struct bNode *node);
        ("group_update_func", c_void_p),
        #
        #/** Initialize a new node instance of this type after creation. */
        #void (*initfunc)(struct bNodeTree *ntree, struct bNode *node);
        ("initfunc", c_void_p),
        #/** Free the node instance. */
        #void (*freefunc)(struct bNode *node);
        ("freefunc", c_void_p),
        #/** Make a copy of the node instance. */
        #void (*copyfunc)(struct bNodeTree *dest_ntree,
        #               struct bNode *dest_node,
        #               const struct bNode *src_node);
        ("copyfunc", c_void_p),
        #/* Registerable API callback versions, called in addition to C callbacks */
        #void (*initfunc_api)(const struct bContext *C, struct PointerRNA *ptr);
        ("initfunc_api", c_void_p),
        #void (*freefunc_api)(struct PointerRNA *ptr);
        ("freefunc_api", c_void_p),
        #void (*copyfunc_api)(struct PointerRNA *ptr, const struct bNode *src_node);
        ("copyfunc_api", c_void_p),
        #
        #/**
        #* Can this node type be added to a node tree?
        #* \param r_disabled_hint: Optional hint to display in the UI when the poll fails.
        #*                         The callback can set this to a static string without having to
        #*                         null-check it (or without setting it to null if it's not used).
        #*                         The caller must pass a valid `const char **` and null-initialize it
        #*                         when it's not just a dummy, that is, if it actually wants to access
        #*                         the returned disabled-hint (null-check needed!).
        #*/
        #bool (*poll)(struct bNodeType *ntype, struct bNodeTree *nodetree, const char **r_disabled_hint);
        ("poll", c_void_p),
        #/** Can this node be added to a node tree?
        #* \param r_disabled_hint: See `poll()`.
        #*/
        #bool (*poll_instance)(struct bNode *node,
        #                    struct bNodeTree *nodetree,
        #                    const char **r_disabled_hint);
        ("poll_instance", c_void_p),
        #/* optional handling of link insertion */
        #void (*insert_link)(struct bNodeTree *ntree, struct bNode *node, struct bNodeLink *link);
        ("insert_link", c_void_p),
        #/* Update the internal links list, for muting and disconnect operators. */
        #void (*update_internal_links)(struct bNodeTree *, struct bNode *node);
        ("update_internal_links", c_void_p),
        #void (*free_self)(struct bNodeType *ntype);
        ("free_self", c_void_p),
        #/* **** execution callbacks **** */
        #NodeInitExecFunction init_exec_fn;
        ("init_exec_fn", c_void_p),
        #NodeFreeExecFunction free_exec_fn;
        ("free_exec_fn", c_void_p),
        #NodeExecFunction exec_fn;
        ("exec_fn", c_void_p),
        #/* gpu */
        #NodeGPUExecFunction gpu_fn;
        ("gpu_fn", c_void_p),
        #/* Expands the bNode into nodes in a multi-function network, which will be evaluated later on. */
        #NodeExpandInMFNetworkFunction expand_in_mf_network;
        ("expand_in_mf_network", c_void_p),
        #/* Execute a geometry node. */
        #NodeGeometryExecFunction geometry_node_execute;
        #("geometry_node_execute", POINTER(NodeGeometryExecFunction)),
        ("geometry_node_execute", c_void_p),
        #/* RNA integration */
        #ExtensionRNA rna_ext;
        
    ]

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

class GeoNodeExecParamsProvider(Structure):
    pass
   
GeoNodeExecParamsProvider._fields_ = [
    
    #public:
    #DNode dnode;
    ("dnode", c_void_p),
    #const PersistentDataHandleMap *handle_map = nullptr;
    ("handle_map", c_void_p),
    #const Object *self_object = nullptr;
    ("self_object", c_void_p),
    #const ModifierData *modifier = nullptr;
    ("modifier", c_void_p),
    #Depsgraph *depsgraph = nullptr;
    ("depsgraph", c_void_p),
    
]
    
class GeoNodeExecParams(Structure):
    pass
   
GeoNodeExecParams._fields_ = [
    # struct bNode *next, *prev, *new_node;
    ("provider_", POINTER(GeoNodeExecParamsProvider)),
]


#NodeGeometryExecFunction = CFUNCTYPE(None, POINTER(GeoNodeExecParams))
#NodeGeometryExecFunction = WINFUNCTYPE(None, c_void_p)
NodeGeometryExecFunction = PYFUNCTYPE(None, c_void_p)


def py_nodeGeometryExecFunction(params):
    pass
    #print("11111")
    #time.sleep(1)
    #print("22222")
    #time.sleep(1)
    #print("33333")
    #time.sleep(1)
    #print("4444")
    #time.sleep(1)
    #print("55555")
    #time.sleep(1)
    #print("py_nodeGeometryExecFunction", params)
    #return 0

nodeGeometryExecFunction = NodeGeometryExecFunction(py_nodeGeometryExecFunction)

def getAddr(func):
    s = str(func)
    start = s.index("0x")
    return int(s[start:-1], 0)

geonodes = bpy.data.node_groups['Geometry Nodes']
groupinput = geonodes.nodes.get("Group Input")
groupoutput = geonodes.nodes.get("Group Output")

tr = geonodes.nodes.get("Transform")


o = bNode.from_address(tr.as_pointer())
"""
o.typeinfo.contents.geometry_node_execute = getAddr(nodeGeometryExecFunction)






o = bNodeSocket.from_address(tr.inputs[0].as_pointer())
show(o)
"""

show(o);