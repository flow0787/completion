{{/*
Expand the name of the chart.
*/}}
{{- define "adaptai-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "adaptai-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "adaptai-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "adaptai-chart.labels" -}}
helm.sh/chart: {{ include "adaptai-chart.chart" . }}
{{ include "adaptai-chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "adaptai-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "adaptai-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Secret name
*/}}
{{- define "adaptai-chart.secret.name" -}}
{{- printf "%s-secret" .Release.Name }}
{{- end }}

{{/*
Service name
*/}}
{{- define "adaptai-chart.service.name" -}}
{{- printf "%s-service" .Release.Name }}
{{- end }}

{{/*
HPA name
*/}}
{{- define "adaptai-chart.hpa.name" -}}
{{- printf "%s-hpa" .Release.Name }}
{{- end }}