# Used for rendering the example gallery. Enables reproducible "clean-room" renders, independent of host OS.
# 
# This is probably compatible with Docker, but I like to use Podman:
#   $ podman build --tag cranim -f Containerfile; podman run --rm -it -v (pwd)/docs:/cranim/tests/examples cranim
#
# Please note that this build-and-render process does take a while to complete.
# Note also that the container will have to be (partially) rebuilt whenever changes are made to cranim.
# Note further that the above command uses fish shell syntax; in Bash, you will instead have to use $(pwd)

FROM fedora:latest

# optimize dnf (helps a lot with downloading texlive)
RUN echo "max_parallel_downloads=20" >> /etc/dnf/dnf.conf
RUN echo "fastestmirror=True" >> /etc/dnf/dnf.conf

# enable RPM fusion (for ffmpeg)
RUN dnf install -y https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

# before installing anything, make sure we're up to date
RUN dnf update -y

# install dependencies and manim
# this includes all the dependencies in https://docs.manim.community/en/stable/installation/linux.html
# plus gcc, which is an undocumented dependency, and vim (which is just nice to have)

RUN dnf install -y texlive-scheme-full  # do this first because it is huge and takes forever
RUN dnf install -y cairo-devel pango-devel python3-devel ffmpeg gcc vim
RUN pip3 install manim

# copy cranim into the container and install it
COPY . /cranim
RUN rm -rf /cranim/examples/
RUN pip3 install -e /cranim

VOLUME /cranim/examples

# on run: render the example gallery
WORKDIR /cranim/tests
CMD ./gallery.py  # comment this out to get a bash shell instead
