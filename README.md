# Drop This

At times, you may want to ignore the output of some function calls.
However, there is the danger of ignoring the wrong values.
For example, consider this code below sending a message through a channel:

```rust
_ = sender.send(msg);
```

Is this correct? Well, it depends on the channel.
Some channels' `send` methods are asynchronous, in that case,
the code above creates a `Future` and ignores it—clearly a mistake;
other channels have a synchronous `send` method, so the code would be correct…

The core problem lies in the fact that `drop` and `_ = …` are type-agnostic,
while you want to be type-aware when ignoring your values.
Therefore, the pro move `drop_this` proposes would be:

```rust
use drop_this::*;
sender.send(msg).drop_result();
```
