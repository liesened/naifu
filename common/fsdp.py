import functools
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
from torch.distributed.fsdp import ShardingStrategy, BackwardPrefetch
from lightning.fabric.strategies import FSDPStrategy


def _strategy():
    from transformers.models.llama.modeling_llama import LlamaDecoderLayer

    auto_wrap_policy = functools.partial(
        transformer_auto_wrap_policy, transformer_layer_cls={LlamaDecoderLayer}
    )
    fsdp_strategy = FSDPStrategy(
        sharding_strategy=ShardingStrategy.FULL_SHARD,
        backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
        forward_prefetch=True,
        auto_wrap_policy=auto_wrap_policy,
        limit_all_gathers=True,
        activation_checkpointing=[LlamaDecoderLayer],
    )
    return fsdp_strategy


def _sd_strategy():
    from models.sgm.model import TimestepEmbedSequential

    fsdp_strategy = FSDPStrategy(
        sharding_strategy=ShardingStrategy.FULL_SHARD,
        backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
        forward_prefetch=True,
        auto_wrap_policy={TimestepEmbedSequential},
        limit_all_gathers=True,
        activation_checkpointing=[TimestepEmbedSequential],
    )
    return fsdp_strategy


def _sd_shard_grad_strategy():
    from models.sgm.model import TimestepEmbedSequential
    
    fsdp_strategy = FSDPStrategy(
        sharding_strategy=ShardingStrategy.SHARD_GRAD_OP, 
        backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
        forward_prefetch=True,
        auto_wrap_policy={TimestepEmbedSequential},
        limit_all_gathers=True,
        activation_checkpointing=[TimestepEmbedSequential],
    )
    return fsdp_strategy

def _sd_hybrid_z2_strategy():
    from models.sgm.model import TimestepEmbedSequential
    
    fsdp_strategy = FSDPStrategy(
        sharding_strategy=ShardingStrategy._HYBRID_SHARD_ZERO2, 
        backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
        forward_prefetch=True,
        auto_wrap_policy={TimestepEmbedSequential},
        limit_all_gathers=True,
        activation_checkpointing=[TimestepEmbedSequential],
    )
    return fsdp_strategy
