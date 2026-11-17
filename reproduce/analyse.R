# Fictional scenario only. Uses base R; no installations or private source files.
args <- commandArgs(trailingOnly=TRUE)
root <- if (length(args)) normalizePath(args[1], mustWork=TRUE) else normalizePath('.')
out <- if (length(args)>1) args[2] else file.path(root,'r_outputs')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
read <- function(name) read.csv(file.path(root,'fictional_inputs',name),check.names=FALSE,stringsAsFactors=FALSE,na.strings=NULL)
write <- function(x,name) write.csv(x,file.path(out,name),row.names=FALSE,na='')
cells <- read('supplier_cells.csv')
reviews <- read('review_decisions.csv')
raw <- read('evidence_rows.csv')
cells$clean_label <- trimws(cells$supplier_raw)
keep <- !cells$clean_label %in% c('','0','Unknown')
excluded <- cells[!keep,]; excluded$Reason <- 'Placeholder, not a candidate label'
occ <- cells[keep,]
labels <- unique(occ[,c('clean_label','technology')])
labels <- labels[order(labels$clean_label),]
labels$LabelID <- paste0('F',sub('Fictional Workshop ','',labels$clean_label))
if (anyDuplicated(reviews$LabelID)) stop('Each label must have exactly one review decision')
if (!setequal(reviews$LabelID, labels$LabelID)) stop('Review IDs must match candidate IDs')
if (any(!raw$LabelID %in% labels$LabelID)) stop('Evidence has an unknown LabelID')
if (anyNA(raw$Year) || any(!nzchar(as.character(raw$Year))) ||
    any(!is.finite(suppressWarnings(as.numeric(raw$Year))))) stop('Every claim needs a numeric reporting year')
if (anyNA(raw$Value) || any(!is.finite(suppressWarnings(as.numeric(raw$Value))))) stop('Claim values must be finite')
if (any(!reviews$Review %in% c('Reviewed','Not reviewed'))) stop('Unknown review status')
if (any(!reviews$Identity %in% c('Resolved','Unresolved'))) stop('Unknown identity status')
labels$Review <- reviews$Review[match(labels$LabelID,reviews$LabelID)]
labels$Identity <- reviews$Identity[match(labels$LabelID,reviews$LabelID)]
stopifnot(!anyNA(labels$Review),!anyDuplicated(labels$LabelID))
duplicates <- raw[duplicated(raw),]
ev <- unique(raw)
assess <- function(review,identity,scope,unit,year) {
  if (review!='Reviewed') return('Unreviewed')
  if (identity!='Resolved') return('Identity unresolved')
  if (scope!='Site') return('Scope mismatch')
  if (!nzchar(unit)) return('Missing unit')
  if (year>2025) return('After cutoff')
  if (year<2023) return('Historical period')
  'Usable example'
}
ev$Assessment <- vapply(seq_len(nrow(ev)),function(i) {
  id <- match(ev$LabelID[i],labels$LabelID)
  assess(labels$Review[id],labels$Identity[id],ev$Scope[i],ev$Unit[i],ev$Year[i])
},'')
severity <- c('Identity unresolved'=1,'Scope mismatch'=1,'Historical period'=2,'After cutoff'=2,'Missing unit'=2,'Unreviewed'=2,'No evidence'=2,'Usable example'=3)
labels$Usable <- vapply(labels$LabelID,function(id) any(ev$LabelID==id & ev$Assessment=='Usable example'),FALSE)
labels$Reason <- vapply(labels$LabelID,function(id) {
  reasons <- ev$Assessment[ev$LabelID==id]
  if (!length(reasons)) return('No evidence')
  reasons[which.min(severity[reasons])]
},'')
labels$Priority <- paste0('P',severity[labels$Reason])
write(labels,'labels.csv');write(ev,'evidence.csv');write(occ,'occurrences.csv');write(excluded,'excluded.csv');write(duplicates,'duplicates.csv')
metrics <- data.frame(Metric=c('candidate_labels','reviewed_labels','usable_labels','follow_up_labels','raw_supplier_cells','occurrences','excluded_placeholders','raw_evidence_rows','evidence_claims','exact_evidence_duplicates','review_coverage','usable_coverage','A_energy_change_pct'),
Value=c(nrow(labels),sum(labels$Review=='Reviewed'),sum(labels$Usable),sum(labels$Priority!='P3'),nrow(cells),nrow(occ),nrow(excluded),nrow(raw),nrow(ev),nrow(duplicates),mean(labels$Review=='Reviewed'),mean(labels$Usable),(ev$Value[ev$LabelID=='FA' & ev$Year==2024]/ev$Value[ev$LabelID=='FA' & ev$Year==2023])-1))
write(metrics,'metrics.csv')
# Acceptance assertions are specified independently from the aggregation code.
stopifnot(nrow(labels)==8,nrow(occ)==10,nrow(ev)==8,nrow(duplicates)==1)
stopifnot(sum(labels$Review=='Reviewed')==6,sum(labels$Usable)==2)
stopifnot(setequal(labels$LabelID[labels$Priority=='P1'],c('FB','FC')))
stopifnot(setequal(labels$LabelID[labels$Priority=='P2'],c('FD','FE','FF','FH')))
stopifnot(setequal(labels$LabelID[labels$Usable],c('FA','FG')))
stopifnot(assess('Reviewed','Resolved','Site','MWh',2026)=='After cutoff')
stopifnot(assess('Reviewed','Resolved','Site','',2024)=='Missing unit')
stopifnot(assess('Reviewed','Unresolved','Site','MWh',2024)=='Identity unresolved')
stopifnot(assess('Not reviewed','Resolved','Site','MWh',2024)=='Unreviewed')
stopifnot(nrow(unique(rbind(labels,labels[1,])))==8)
cat('PASS: raw reconciliation, exact duplicate policy, priority membership and edge rules.\n')
print(metrics,row.names=FALSE)
