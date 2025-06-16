output "target_group_arn" {
  value       = "${aws_alb_target_group.target_group.arn}"
  description = "The ARN of the target group"
}

output "dns_name" {
  value       = "${aws_route53_record.dns_record.fqdn}"
  description = "The DNS name for the service."
}
