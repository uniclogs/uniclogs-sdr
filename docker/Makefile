.DEFAULT_GOAL := help

all: ## run all, build and up (down)
	$(MAKE) up
  
build: ## build gnuradio system
	docker build . -t uniclogs-sdr

up: | build down ## bring up gnuradio system
	docker-compose up -d

down: ## bring down gnuradio system
	docker-compose down -v --remove-orphans

shell: build ## shell into gnuradio container
	docker-compose up -d && docker run -it uniclogs-sdr "bash"

help:
	@printf "\033[37m%-30s\033[0m %s\n" "#----------------------------------------------------------------------------------"
	@printf "\033[37m%-30s\033[0m %s\n" "# Makefile                                          "
	@printf "\033[37m%-30s\033[0m %s\n" "#----------------------------------------------------------------------------------"
	@printf "\033[37m%-30s\033[0m %s\n" "#-targets----------------------description-----------------------------------------"
	@grep -E '^[a-zA-Z_-].+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo $* = $($*)
