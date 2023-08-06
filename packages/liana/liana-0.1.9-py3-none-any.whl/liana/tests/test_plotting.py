import numpy as np
from liana.plotting import dotplot, dotplot_by_sample
from liana.testing import sample_lrs

liana_res = sample_lrs()


def test_check_dotplot_order():
    my_p = dotplot(liana_res=liana_res,
                   size='specificity_rank',
                   colour='magnitude',
                   top_n=20,
                   orderby='specificity_rank',
                   orderby_ascending=False,
                   target_labels=["A", "B", "C"]
                   )
    assert my_p is not None
    assert 'interaction' in my_p.data.columns
    np.testing.assert_equal(np.unique(my_p.data.interaction).shape, (20,))
    set(my_p.data.target)
    assert {'A', 'B', 'C'} == set(my_p.data.target)


def test_check_doplot_filter():
    my_p2 = dotplot(liana_res=liana_res,
                    size='specificity_rank',
                    colour='magnitude',
                    filterby='specificity_rank',
                    filter_lambda=lambda x: x > 0.95,
                    inverse_colour=True,
                    source_labels=["A"]
                    )
    assert my_p2 is not None
    # we force this, but not intended all interactions
    # to be only 0.95, but rather for an interaction to get
    # plotted, in at least one cell type pair it should be > 0.95
    assert all(my_p2.data['specificity_rank'] > 0.95) is True


def test_dotplot_bysample():
    liana_res = sample_lrs(by_sample=True)
    my_p3 = dotplot_by_sample(liana_res=liana_res,
                              size='specificity_rank',
                              colour='magnitude',
                              target_labels='E',
                              sample_key='sample')
    assert my_p3 is not None
    assert 'interaction' in my_p3.data.columns
    assert 'sample' in my_p3.data.columns
    assert 'B' not in my_p3.data['target']
    
    