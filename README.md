# Heston Stochastic Volatility Simulator Skill

Two-factor coupled stochastic differential equation solver featuring CIR variance and correlated Brownian noise.

```mermaid
flowchart TD
    Gaussian["Correlated Gaussians (Z1, Z2 with correlation ρ)"] --> Var["CIR Variance Step: dV = κ(θ - V)dt + ξ √V dW_V"]
    Gaussian --> Price["Price Step: dS = μ S dt + √V S dW_S"]
    Var --> Price
    Var --> Feller["Feller Verification: 2κθ > ξ^2"]
```

## Features
- **100% Python Standard Library**: Full truncation Euler scheme for non-negative variance.
- **Correlated Noise Injection**: Cholesky decomposition of 2D Wiener processes.
- **Feller Boundary Check**: Automatic analytical positivity verification.
