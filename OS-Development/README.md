# OS Development

This is the main OS that I am going to be creating

## Some Note

Before running use the docker environment file in the buildenv folder to initialize the environment
If the environment is not created use this code
`
docker build buildenv -t myos-buildenv
`

Then run the docker file
``
docker run --rm -it -v "$(pwd)":/root/env myos-buildenv //For Linux and Mac
docker run --rm -it -v "%cd%":/root/env myos-buildenv // For Windows (CMD)
``

