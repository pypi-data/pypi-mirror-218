from typing import Any, Dict

import torch

from .base import TaskEngine
from ..datasets.utils import tensor_to_numpy
from ..metrics.extraction.span import SpanEvaluator
from ..nn.uie import UIEModel


class UieEngine(TaskEngine):

    def get_auto_model(self, downstream_model_type, downstream_model_name):
        return UIEModel

    def common_step(self, batch: Any):
        outputs = self.model(**batch)
        start_prob = tensor_to_numpy(outputs.start_prob)
        end_prob = tensor_to_numpy(outputs.end_prob)

        start_ids = tensor_to_numpy(batch['start_positions'].to(torch.float32))
        end_ids = tensor_to_numpy(batch['end_positions'].to(torch.float32))

        num_correct, num_infer, num_label = self.metric.compute(
            start_prob, end_prob, start_ids, end_ids,
        )
        self.metric.update(num_correct, num_infer, num_label)

    def common_epoch_end(self, prefix: str):
        metric_dict = self.compute_metrics(mode=prefix)
        self.log_dict(metric_dict, prog_bar=True, on_step=False, on_epoch=True)
        return metric_dict

    def validation_step(self, batch: Any, batch_idx: int, dataloader_idx: int = 0):
        return self.common_step(batch)

    def on_validation_epoch_end(self):
        return self.common_epoch_end("val")

    def test_step(self, batch: Any, batch_idx: int, dataloader_idx: int = 0):
        return self.common_step(batch)

    def on_test_epoch_end(self):
        return self.common_epoch_end("test")

    def configure_metrics(self, _) -> None:
        self.metric = SpanEvaluator()

    def compute_metrics(self, mode="val") -> Dict[str, float]:
        p, r, f = self.metric.accumulate()
        self.metric.reset()
        return {f"{mode}_precision": p, f"{mode}_recall": r, f"{mode}_f1_micro": f}
