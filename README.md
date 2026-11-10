# SAM 3.1 weights

Unmodified copies of Meta's model weights, stored directly in this git repository. Upstream: https://github.com/facebookresearch/sam3

**License:** these files are distributed under Meta's SAM License, see [LICENSE](LICENSE).
By downloading or using them you agree to those terms. This mirror does not relicense anything.

## Get the weights

Everything is in the repo itself (no releases, no Git LFS). GitHub allows at most 100 MB per file,
so each large file is stored as `<name>.part000`, `<name>.part001`, ... next to its config files.

```
git clone --depth 1 https://github.com/SchockTop/sam3.1-weights.git
cd sam3.1-weights
python join.py
```

`join.py` works offline (standard library only): it joins the parts into the model files below and checks
the SHA256. `python join.py --only <folder>` joins one variant, `--delete-parts` frees the space afterwards.

Without Python, join by hand and compare the SHA256 with the table:

```
:: Windows (cmd)
copy /b "sam3.1\sam3.1_multiplex.pt.part*" "sam3.1\sam3.1_multiplex.pt"
certutil -hashfile "sam3.1\sam3.1_multiplex.pt" SHA256

# Linux / macOS
cat sam3.1/sam3.1_multiplex.pt.part* > sam3.1/sam3.1_multiplex.pt && sha256sum sam3.1/sam3.1_multiplex.pt
```

## Contents

- `sam3.1/`: original `sam3.1_multiplex.pt` checkpoint + tokenizer/config files
- `sam3.1-image-hf/`: image model in Hugging Face `transformers` format (`model.safetensors` + configs)

| File | Size | Parts | SHA256 |
|---|---|---|---|
| `sam3.1/sam3.1_multiplex.pt` | 3.50 GB | 36 | `0567debeec80ba4ac6369540c6c248025283cb3ff2b92827509e57e2b3541cb6` |
| `sam3.1-image-hf/model.safetensors` | 3.36 GB | 34 | `6d53087688a238117da97e307581ad062559259eef0860b0bce5f77c286a70af` |

`.pt` / `.pth` files are pickle based: load them with `torch.load(..., weights_only=True)`.
