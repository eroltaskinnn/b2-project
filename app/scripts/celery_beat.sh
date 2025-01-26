#!/bin/bash
celery -A tasks.library_tasks beat -l info


