# Copyright Contributors to the Pyro project.
# SPDX-License-Identifier: Apache-2.0

import pytest
import torch

from pyro.ops.special import log_beta, log_binomial


@pytest.mark.parametrize("tol", [
    1e-8, 1e-6, 1e-4, 1e-2, 0.02, 0.05, 0.1, 0.2, 0.1, 1.,
])
def test_log_beta_stirling(tol):
    x = torch.logspace(-5, 5, 200)
    y = x.unsqueeze(-1)

    expected = log_beta(x, y)
    actual = log_beta(x, y, tol=tol)

    assert (actual <= expected).all()
    assert (expected < actual + tol).all()


@pytest.mark.parametrize("tol", [
    1e-8, 1e-6, 1e-4, 1e-2, 0.02, 0.05, 0.1, 0.2, 0.1, 1.,
])
def test_log_binomial_stirling(tol):
    k = torch.arange(200.)
    n_minus_k = k.unsqueeze(-1)
    n = k + n_minus_k

    # Test binomial coefficient choose(n, k).
    expected = (n + 1).lgamma() - (k + 1).lgamma() - (n_minus_k + 1).lgamma()
    actual = log_binomial(n, k, tol=tol)

    assert (actual - expected).abs().max() < tol
