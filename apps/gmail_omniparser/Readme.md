# Gmail OmniParser: Screen Parsing tool for Vision Based Gmail Agent

## Install Python

Install Python (3.12)

- https://www.python.org/downloads/

## ## (Linux Only) Pre-Setup
```shell
cd apps/gmail_omniparser
conda create -n "omni" python==3.12
conda activate omni
pip install -r requirements.txt
```

## (MacOS & Windows) Pre-Setup
```shell
cd apps/gmail_omniparser
python3.12 -m venv omni
source omni/bin/activate
pip install -r requirements.txt
```

## Download Model Weights (Linux)
Ensure you have the V2 weights downloaded in weights folder (ensure caption weights folder is called icon_caption_florence). If not download then run below:-
```shell
# download the model checkpoints to local directory OmniParser/weights/
for f in icon_detect/{train_args.yaml,model.pt,model.yaml} icon_caption/{config.json,generation_config.json,model.safetensors}; do huggingface-cli download microsoft/OmniParser-v2.0 "$f" --local-dir weights; done
```
```shell
mv weights/icon_caption weights/icon_caption_florence
```
## Download model Weights (Windows & Mac)
```shell
for %f in (icon_detect/train_args.yaml icon_detect/model.pt icon_detect/model.yaml icon_caption/config.json icon_caption/generation_config.json icon_caption/model.safetensors) do huggingface-cli download microsoft/OmniParser-v2.0 "%f" --local-dir weights
```
```shell
rename weights\icon_caption icon_caption_florence
```
## Gradio Demo
It,s just screenshot based icons detection demo.
```python
python gradio_demo.py
```