import io

with io.open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# The table was duplicated because b9af2a1 already had it!
# I will find the first occurrence and remove the duplicate if it exists.
dup_str = """### Threshold Sensitivity

To demonstrate 0.29 is genuinely optimal and not cherry-picked:

<div align="center">

| Threshold | Precision | Recall | F1 | Notes |
|:---------:|:---------:|:------:|:--:|:------|
| 0.20 | ~47% | ~97% | ~63% | Too aggressive — too many weak defenses filed |
| 0.25 | ~55% | ~94% | ~69% | Still recall-heavy |
| **0.29** | **62.3%** | **90.2%** | **73.7%** | ✅ **Cost-optimal on validation set** |
| 0.35 | ~70% | ~85% | ~77% | Higher precision but misses more winnable disputes |
| 0.40 | ~75% | ~78% | ~76% | Approaching balance — costs rise due to FN |
| 0.50 | ~82% | ~65% | ~73% | Default — suboptimal given cost asymmetry |

</div>"""

if content.count(dup_str) > 1:
    # Replace the FIRST occurrence with nothing, leaving exactly one.
    content = content.replace(dup_str, "", 1)

with io.open("README.md", "w", encoding="utf-8") as f:
    f.write(content)
print("Deduplicated")
