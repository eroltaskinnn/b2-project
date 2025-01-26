#!/bin/bash

celery -A tasks.library_tasks worker --loglevel=info


