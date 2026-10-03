We are using a Dockerfile for training a model with minicpm5-2b (a variant of the MiniCPM series).
 The base image is `openbmb/minicpm5-2b:latest`.
 We set a parameter `num_ctx` to 16384 (which is 256M tokens, typical for large models).

 However, note that the original question had two parts:

 1. Running `minicpm5-2b.json` from its directory (likely for some setup or training)
 2. Then using `minicpm5-2b-training.sh` as a follow-up command

 But in this Dockerfile, we are just setting a parameter and not running scripts directly.

 Let's construct a Dockerfile that:

- Uses the base image `openbmb/minicpm5-2b:latest`
- Sets environment variables or parameters accordingly
- Optionally, we can copy the config and scripts into the image for training

 However, note that the user's initial request was to:

  1. Run `minicpm5-2b.json` from its directory
  2. Then run `minicpm5-2b-training.sh`

 So, we can either:

- Build the image with these scripts copied in, and then run them from the container.
- Or, we can design the Dockerfile to set up the environment and then run the scripts.

 Since the user mentioned "two steps", let's assume they want the Dockerfile to be built first,
 and then they will run the training from within the container.

 Alternatively, if they want to run the scripts from the host machine before building,
 we could copy the files and then use the Dockerfile to build the image.

 But note: the user's original instruction was to "set up the Dockerfile for training",
 so let's make it clear.

 We'll provide two options:

 Option A: Build the image with the scripts baked in (recommended for training)

- Copy the config and training script into the image
- Set any necessary parameters in the Dockerfile

 Option B: Build the image without scripts, and then run them from the host before building

- This might be useful if the training script needs to run with some environment variables
     that are set in the host environment and not captured inside the container.

 However, the typical pattern for Docker-based training is Option A.

 Let's assume the user wants Option A, but we'll also note Option B.

 Since the user's question was about how to "write a Dockerfile for training",
 I'll provide a complete Dockerfile that includes both steps (config and training script) and also
 sets the parameter.

 If the user wants to run the scripts from the host machine before building, they can do:

  1. Copy the config and training script to the Dockerfile build context
  2. Build the image
  3. Run the training script from within the container

 Alternatively, if they don't want to bake the scripts into the image, they can use the Dockerfile
 to set the base image and parameters, and then copy the scripts into the container.

 Let me provide two Dockerfiles:

 Option A: With baked-in scripts (best for training)

   FROM openbmb/minicpm5-2b:latest
   COPY minicpm5-2b.json /tmp/minicpm5-2b.json
   COPY minicpm5-2b-training.sh /tmp/minicpm5-2b-training.sh
   RUN chmod +x /tmp/minicpm5-2b-training.sh
   ENV num_ctx 16384

   Then run: docker exec <container_name> bash -c /tmp/minicpm5-2b-training.sh

 Option B: Without baked-in scripts, but with base image and parameters

   FROM openbmb/minicpm5-2b:latest
   PARAMETER num_ctx 16384

   This Dockerfile does not include the scripts. The user would then copy them separately and
   build a second image or run them from the host before building a combined image.

 Since the user said "set up a Dockerfile for training", I think they want Option A.

 However, note that the base image might already have some scripts or configurations.
 Let's assume we need to copy the config and training script.

 Final Dockerfile for Option A:

   FROM openbmb/minicpm5-2b:latest
   COPY minicpm5-2b.json /tmp/minicpm5-2b.json
   COPY minicpm5-2b-training.sh /tmp/minicpm5-2b-training.sh
   RUN chmod +x /tmp/minicpm5-2b-training.sh
   ENV num_ctx 16384

   This sets the base image, copies the config and training script, sets permissions,
   and sets the environment variable.

   Then build: docker build -t minicpm5-2b training/

   Then run: docker run -it minicpm5-2b bash

   And from within the container, run the training script:
      /tmp/minicpm5-2b-training.sh

 However, note that the user's original question also mentioned running the config file
 (`minicpm5-2b.json`) separately. In Option A, we are copying the config into the container.

 If the user wants to run the config file from the host (as a separate step) and then run the training script,
 we can do:

   Step 1: docker build -t minicpm5-2b training/

   Step 2: docker run -it minicpm5-2b /tmp/openbmb/minicpm5-2b/setup.sh   (if there is such a script)
   Step 3: docker run -it minicpm5-2b /tmp/minicpm5-2b.json   (if the config is used as a file)

   But note: the user's example Dockerfile does not have any such step. We are copying the files
   in the image, so the training script can read them from the container filesystem.

 So, if the user's training script needs to read the config and run the training, we don't need
 a separate step for that because the files are in the image.

 Let me adjust the Dockerfile to also include the base image setup for the minicpm5-2b model.

 Since the base image is `openbmb/minicpm5-2b:latest`, it might already include a systemd unit
 or some other initialization. We just need to copy the config and training script.

 If there are other files to copy, the user can add them with additional COPY commands.

 So, the final Dockerfile (Option A) is:

   FROM openbmb/minicpm5-2b:latest
   COPY minicpm5-2b.json /tmp/minicpm5-2b.json
   COPY minicpm5-2b-training.sh /tmp/minicpm5-2b-training.sh
   COPY other_files /tmp/   # if needed
   RUN chmod +x /tmp/minicpm5-2b-training.sh
   ENV num_ctx 16384
   EXPOSE 8080   # if the training script listens on a port

   Then build and run as described.

 However, the user's original instruction also mentioned running the config file from its directory.
 This might mean they want to run the config file from the host machine to generate
 a configuration file, or it might mean they want to run the config file in the container
 as a separate step.

 Without more context, I'll assume the latter: the training script (`minicpm5-2b-training.sh`)
 reads the config file from the container and uses it to run training.

 If the user wants to run the config file from the host, they can do:

   docker run -it minicpm5-2b bash -c "cat minicpm5-2b.json | cp /tmp/config.json /tmp/"

 But that's not necessary if we copy the file in the Dockerfile.

 So, the Dockerfile I provided (Option A) is comprehensive.

 Let me also note that the user's original question had a Dockerfile example with only the base image
 and a parameter. Without the scripts, it's incomplete for training. So, I'll provide both options
 in my response.

 However, since the user asked to "set up a Dockerfile", I'll assume they want the complete
 Dockerfile for training with the scripts baked in.

 If the user wants to run the scripts from the host before building, they can remove the COPY
 instructions and use the environment variables instead.

 Let me provide two versions:

 Version 1: With scripts (for building an image with everything pre-configured)

   FROM openbmb/minicpm5-2b:latest
   COPY minicpm5-2b.json /tmp/minicpm5-2b.json
   COPY minicpm5-2b-training.sh /tmp/minicpm5-2b-training.sh
   COPY other_files /tmp/   # add other files as needed
   RUN chmod +x /tmp/minicpm5-2b-training.sh
   ENV num_ctx 16384
   EXPOSE 8080   # optional, if your training script uses a port

   RUN /tmp/minicpm5-2b-training.sh   # if you want to run it after the container starts

   This would run the training script immediately after container creation.
   But note: some training scripts might need to wait for other setup, so using `docker run` with
   a sleep or using `--init` might be better.

 Version 2: Without baked-in scripts (for building an image and then running from host)

   FROM openbmb/minicpm5-2b:latest
   PARAMETER num_ctx 16384
   COPY minicpm5-2b.json /tmp/config.json
   COPY minicpm5-2b-training.sh /tmp/training.sh
   RUN chmod +x /tmp/training.sh
   ENV num_ctx 16384

   Then build and run from the host:

     docker run -it --rm minicpm5-2b /tmp/training.sh

   Or better, run it after the container starts (without --rm):

     docker run -it minicpm5-2b /tmp/training.sh

   But note: the training script might depend on other files that are also in the container,
   which are copied in by the COPY instruction above. If there are other files, you need to
   add them in additional COPY instructions.

 Since the user's question was about "setting up" the Dockerfile, I'll present Version 1
 as the primary answer and Version 2 as an alternative.

 However, note that the user's original example Dockerfile (with just base image and parameter)
 was the first example they provided. Without the scripts, it's incomplete for training.

 So, I'll answer:

 To set up a Dockerfile for training, you can either:

 1. Include the training scripts in the Dockerfile (preferred for production training):

   FROM openbmb/minicpm5-2b:latest
   COPY minicpm5-2b.json /tmp/minicpm5-2b.json
   COPY minicpm5-2b-training.sh /tmp/minicpm5-2b-training.sh
   COPY other_files /tmp/   # other files to include
   RUN chmod +x /tmp/minicpm5-2b-training.sh
   ENV num_ctx 16384
   EXPOSE 8080
   RUN /tmp/minicpm5-2b-training.sh   # optionally run after build

 1. Or, keep the base image and parameters, and copy the scripts separately before building:

   FROM openbmb/minicpm5-2b:latest
   PARAMETER num_ctx 16384
   COPY minicpm5-2b.json /tmp/config.json
   COPY minicpm5-2b-training.sh /tmp/training.sh
   RUN chmod +x /tmp/training.sh
   ENV num_ctx 16384

   Then build the image with these changes, and then run the training script from the host
   with `docker run -it <image_name> /tmp/training.sh`

 The choice depends on whether you want the training scripts baked into the image or kept on
 the host.

 For training, it's often better to bake the scripts into the image so that they don't rely
 on host-specific environment variables.

 However, the user's original question also mentioned running the config file from its directory.
 This might mean they want to run the config file in the container for configuration, or it
 might be a separate step (like running the config file from the host to generate a config
 file). Without more context, I'll assume they want to run the config file from the host
 (maybe to update the config file with current information) and then run the training script.

 Let me also provide:

   To run the config file from the host, you can do:

     docker run -it openbmb/minicpm5-2b bash -c "cp /path/to/minicpm5-2b.json /tmp/"

   Then copy the config into the image with the COPY instruction above.

   Or, if the config file is already in the image, you might not need a separate step.

 Since the user's example Dockerfile did not include the config or training script, I'll
 assume they need to copy them in during the build process.

 My final answer will provide both versions and explain the trade-offs.

 However, note that the user's original question also mentioned "how to run" the Dockerfile.
 So, I'll include instructions for both building and running.

 Let me write the answer in a structured way.
</think>

To set up a Dockerfile for training **MiniCPM-2B**, you need to combine the base image, necessary files (config + training
script), and environment parameters. Here's a practical approach:

### **Option 1: Complete Dockerfile with all training artifacts baked in**

```dockerfile
FROM openbmb/minicpm5-2b:latest
ENV num_ctx 16384
COPY training_pipeline/ /workspace/    # copy config + scripts
RUN chmod +x /workspace/train.sh
```

**Key steps:**

1. **Copy your project files** (`config.json`, `train.sh`, etc.) into the image root.
2. **Set environment variables** (like `num_ctx`) directly in the Dockerfile.
3. **Run after build:**

   ```bash
   docker build -t minicpm5-2b .
   docker run -it --rm minicpm5-2b /workspace/train.sh
   ```

---

### **Option 2: Minimal Dockerfile + manual copy on host**

```dockerfile
FROM openbmb/minicpm5-2b:latest
ENV num_ctx 16384
WORKDIR /workspace
COPY config.json training.sh ./   # manual step before build
```

**Build/run on your host (before Docker build):**

```bash
cp config.json training.sh /workspace/
docker build -t minicpm5-2b .
```

---

### **Why this pattern?**

- **Base image**: `openbmb/minicpm5-2b:latest` provides the model weights and dependencies.
- **Environment variables**: Control hyperparameters (`num_ctx`, batch size, etc.).
- **COPY timing**: Copy config/training files **before** running `docker run` if they need fresh data from the host, but
include them in the Dockerfile for reproducible builds.

### **Verification**

```bash
# Test inside container
docker run --rm minicpm5-2b cat /workspace/config.json
docker run --rm minicpm5-2b env | grep num_ctx
```
