from keras_core.src import backend
from keras_core.src import ops
from keras_core.src.api_export import keras_core_export
from keras_core.src.layers.layer import Layer


@keras_core_export("keras_core.layers.AlphaDropout")
class AlphaDropout(Layer):
    """Applies Alpha Dropout to the input.

    Alpha Dropout is a kind of dropout that keeps mean and variance of inputs
    to their original values, in order to ensure the self-normalizing property
    even after this dropout.
    Alpha Dropout fits well to Scaled Exponential Linear Units
    by randomly setting activations to the negative saturation value.

    Args:
        rate: float, drop probability (as with `Dropout`).
            The multiplicative noise will have
            standard deviation `sqrt(rate / (1 - rate))`.
        noise_shape: 1D integer tensor representing the shape of the
            binary dropout mask that will be multiplied with the input.
            For instance, if your inputs have shape
            `(batch_size, timesteps, features)` and
            you want the dropout mask to be the same for all timesteps,
            you can use `noise_shape=(batch_size, 1, features)`.
        seed: A Python integer to use as random seed.

    Call arguments:
        inputs: Input tensor (of any rank).
        training: Python boolean indicating whether the layer should behave in
            training mode (adding dropout) or in inference mode (doing nothing).
    """

    def __init__(self, rate, noise_shape=None, seed=None, **kwargs):
        super().__init__(**kwargs)
        self.rate = rate
        self.noise_shape = noise_shape
        self.seed = seed
        self.seed_generator = backend.random.SeedGenerator(seed)
        self.supports_masking = True

    def call(self, inputs, training=False):
        if training and 0.0 < self.rate < 1.0:
            alpha = 1.6732632423543772848170429916717
            scale = 1.0507009873554804934193349852946
            alpha_p = -alpha * scale

            noise_shape = (
                self.noise_shape if self.noise_shape else ops.shape(inputs)
            )

            kept_idx = ops.greater_equal(
                backend.random.uniform(noise_shape, seed=self.seed_generator),
                self.rate,
            )
            kept_idx = ops.cast(kept_idx, dtype=inputs.dtype)

            # Get affine transformation params
            a = ((1 - self.rate) * (1 + self.rate * alpha_p**2)) ** -0.5
            b = -a * alpha_p * self.rate

            # Apply mask
            x = inputs * kept_idx + alpha_p * (1 - kept_idx)

            # Do affine transformation
            return a * x + b
        return inputs

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_config(self):
        base_config = super().get_config()
        config = {
            "rate": self.rate,
            "seed": self.seed,
            "noise_shape": self.noise_shape,
        }
        return {**base_config, **config}

