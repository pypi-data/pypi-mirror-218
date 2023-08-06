

def build_dvc_demo1():
    """
    Builds a medium complexity dvc repo, todo:
        implement some tests
    """
    import ubelt as ub
    from simple_dvc import SimpleDVC
    import random

    rng = random.Random(10998676167967)

    demo_root = ub.Path.appdir('simpledvc', 'demos', 'demo1')

    precon_dpath = ub.Path.appdir('simpledvc', 'precon')
    precon_dvc_root = precon_dpath / 'demo1'

    precon_stamp = ub.CacheStamp('demo1_precon', dpath=precon_dpath,
                                 depends=['v1'])
    if precon_stamp.expired() or not precon_dvc_root.exists():
        # Build in a staging area first
        dvc_root = precon_dvc_root
        dvc_root.delete()
        SimpleDVC.init(dvc_root, no_scm=True)

        dvc = SimpleDVC.coerce(dvc_root)

        # Build basic data
        (dvc_root / 'test-set1').ensuredir()
        assets_dpath = (dvc_root / 'test-set1/assets').ensuredir()
        for idx in range(1, 21):
            fpath = assets_dpath / f'asset_{idx:03d}.data'
            fpath.write_text(str(idx) * 100)
        manifest_fpath = (dvc_root / 'test-set1/manifest.txt')
        manifest_fpath.write_text('pretend-data')

        root_fpath = dvc_root / 'root_file'
        root_fpath.write_text('----' * 100)

        root_dpath = dvc_root / 'root_dir'

        node_paths = random_nested_paths(rng=rng)

        for node_path in node_paths:
            rel_fpath = ub.Path(*[f'dir_{n}' for n in node_path[0:-1]]) / ('file_' + str(node_path[-1]) + '.data')
            fpath = root_dpath / rel_fpath
            fpath.parent.ensuredir()
            fpath.write_text(str(node_path))

        dvc.add(root_dpath)
        dvc.add(root_fpath)
        dvc.add(manifest_fpath)
        dvc.add(assets_dpath)

        precon_stamp.renew()

        # import xdev
        # xdev.tree_repr(dvc_root)

    demo_root.delete()
    demo_root.parent.ensuredir()
    precon_dvc_root.copy(demo_root)
    return demo_root


def random_nested_paths(num=30, rng=None):
    # Use networkx to make a random complex directory structure
    import networkx as nx
    graph = nx.erdos_renyi_graph(num, p=0.2, directed=True, seed=rng)
    tree = nx.minimum_spanning_arborescence(graph)
    nx.write_network_text(tree)
    sources = [n for n in tree.nodes if not tree.pred[n]]
    sinks = [n for n in tree.nodes if not tree.succ[n]]

    node_paths = []
    for t in sinks:
        for s in sources:
            paths = list(nx.all_simple_edge_paths(tree, s, t))
            if paths:
                node_path = [u for (u, v) in paths[0]] + [t]
                node_paths.append(node_path)
    return node_paths
