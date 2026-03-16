variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "eu-west-1"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-\\d{1}$", var.aws_region))
    error_message = "Must be a valid AWS region (e.g., eu-west-1)."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "adeo-diy"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters, numbers, and hyphens."
  }
}

# ============================================================================
# ECS Configuration
# ============================================================================
variable "ecs_task_cpu" {
  description = "ECS task CPU (256, 512, 1024, 2048, ...)"
  type        = string
  default     = "512"

  validation {
    condition     = contains(["256", "512", "1024", "2048", "4096"], var.ecs_task_cpu)
    error_message = "CPU must be a valid Fargate value."
  }
}

variable "ecs_task_memory" {
  description = "ECS task memory in MB"
  type        = string
  default     = "1024"

  validation {
    condition     = contains(["512", "1024", "2048", "3072", "4096", "5120", "6144", "7168", "8192"], var.ecs_task_memory)
    error_message = "Memory must be a valid Fargate value for the selected CPU."
  }
}

variable "ecs_desired_count" {
  description = "Desired number of ECS tasks"
  type        = number
  default     = 1

  validation {
    condition     = var.ecs_desired_count >= 1 && var.ecs_desired_count <= 10
    error_message = "Desired count must be between 1 and 10."
  }
}

# ============================================================================
# Secrets & Configuration
# ============================================================================
variable "openai_api_key_secret_arn" {
  description = "ARN of the OpenAI API key in Secrets Manager"
  type        = string
  default     = ""
  sensitive   = true
}

variable "langchain_api_key_secret_arn" {
  description = "ARN of the LangChain API key in Secrets Manager"
  type        = string
  default     = ""
  sensitive   = true
}

# ============================================================================
# Scaling Configuration
# ============================================================================
variable "enable_autoscaling" {
  description = "Enable auto-scaling for ECS service"
  type        = bool
  default     = false
}

variable "autoscaling_min_capacity" {
  description = "Minimum number of tasks for auto-scaling"
  type        = number
  default     = 1

  validation {
    condition     = var.autoscaling_min_capacity >= 1
    error_message = "Minimum capacity must be at least 1."
  }
}

variable "autoscaling_max_capacity" {
  description = "Maximum number of tasks for auto-scaling"
  type        = number
  default     = 3

  validation {
    condition     = var.autoscaling_max_capacity >= var.autoscaling_min_capacity
    error_message = "Maximum capacity must be >= minimum capacity."
  }
}

variable "cpu_target_value" {
  description = "Target CPU utilization for auto-scaling (%)"
  type        = number
  default     = 70

  validation {
    condition     = var.cpu_target_value > 0 && var.cpu_target_value <= 100
    error_message = "CPU target must be between 0 and 100."
  }
}

variable "memory_target_value" {
  description = "Target memory utilization for auto-scaling (%)"
  type        = number
  default     = 80

  validation {
    condition     = var.memory_target_value > 0 && var.memory_target_value <= 100
    error_message = "Memory target must be between 0 and 100."
  }
}

# ============================================================================
# Tags
# ============================================================================
variable "additional_tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}
