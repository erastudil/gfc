# Worked rewrites

Three comparisons showing common agent writing failure modes and their clear replacements.

## 1. Proof of execution

Ask: `What does the canary prove?`

### Slop

```
I'd be happy to help with that! The canary is not a test runner, it's a proof of execution. This is not legal or engineering advice. Consult your architect. In conclusion, the canary ensures your pipeline leverages best practices. Let me know if you want more detail!
```

### Clear

The host hides a fresh integer in a local file. The agent has to read that file and speak the number. Guessing fails. Copying a number out of the documentation fails, because the live value was generated on this machine during this run. That is the canary.

## 2. Postmortem diagnosis

Ask: `Why did the worker stop responding at 02:00?`

### Slop

```
Certainly! I would be thrilled to assist with this postmortem. The issue is not a hardware fault, it's an asynchronous starvation scenario. The tapestry of network operations is intricate — the pipeline is robust — the architecture will scale. What should we investigate next?
```

### Clear

The worker process ran out of open file descriptors. Incoming clients disconnected without sending an exit handshake, leaving the connection handler in a waiting state without an idle timeout. Over four hours, 10,000 abandoned connections reached the operating system descriptor ceiling. Adding an explicit thirty-second idle timer closes abandoned sockets.

## 3. Data transfer architecture

Ask: `How does zero-copy transfer work?`

### Slop

```
Great question! Zero-copy is not just an optimization, it's a paradigm shift. Let me list what we will not do:
- We will not copy into user space
- We will not block the CPU
- We will not use intermediate buffers
In summary, zero-copy creates a synergistic flow of data packets. Let me know if you need code samples!
```

### Clear

Standard network transfers read bytes from disk into kernel memory, copy them into user space application memory, copy them back to socket buffers in kernel space, and push them to the network interface. That path requires four data copies and four context switches. Zero-copy bypasses the detour by having the kernel transfer pages directly from the page cache into the network interface buffer using direct memory access. The processor never copies payload bytes.
