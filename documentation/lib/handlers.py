##############################################################################
# handlers.py                                                                #
##############################################################################

# The following symbols are imported using magic:
#
# import uriel
# from uriel import Page
# from uriel import Node
# from uriel import FileNode
# from uriel import VirtualNode
# from uriel import HandlerError
# from uriel import log
# from uriel import escape

#def init(project_root):
#    pass

def before_render_node_tree(project_root, root_node):
    # find the node for the Handlers page
    # (the nodes/handlers file)
    example_root = root_node.find_node_by_path("handlers")

    # create a new virtual node under the Handers page, with the node path
    # "handlers/virtual", as a child of the "handlers" node
    vnode = VirtualNode(project_root,
                        example_root.get_path() + "/virtual",
                        example_root)

    # add the VirtualNode to the list of child nodes for the parent
    # "handlers" node
    example_root.add_child(vnode)

    # N.B. we need to add the parent node in the VirtualNode constructor, and
    #      also call the add_child() method on the parent node, so that the
    #      parent/child relationship is established in both directions

    # set the Title and RSS-Include headers for this vnode
    #
    # uriel canonicalizes all header names to lowercase internally, so we
    # set headers in all lowercase when creating vnodes
    vnode.set_header("title", "VirtualNode Example")
    vnode.set_header("rss-include", "true")

    # set the node body contents
    vnode.set_body(
        "<p>Hello from a VirtualNode.</p>\n" +
        "\n" +
        "<p>See the {{node-link:handlers}} page for more details.</p>"
    )

def after_render_node_tree(project_root, root_node):
    # find the node for the virtual node we created earlier in the
    # before_render_node_tree() handler function
    vnode = root_node.find_node_by_path("handlers/virtual")

    # get the node body
    body = vnode.get_body()

    # modify our local copy of the node body contents
    body += "\n\n<p>This is a special message for RSS readers only.</p>"

    # set the node body to our modified string
    vnode.set_body(body)

#def cleanup(project_root, root_node):
#    pass

