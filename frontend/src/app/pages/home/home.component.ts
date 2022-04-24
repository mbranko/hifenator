import { Component, OnInit, ViewChild } from '@angular/core';
import { PrimeNGConfig, MessageService } from 'primeng/api';
import { FileUpload } from 'primeng/fileupload';
import { FileService } from '../../services/file';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  fileIds: number[] = [];
  resultFiles: any[] = [];
  refreshTimer: any;
  @ViewChild(FileUpload) fileUpload!: FileUpload;

  constructor(
    private primengConfig: PrimeNGConfig,
    private messageService: MessageService,
    private fileService: FileService,
  ) { }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.fileIds = [];
    this.resultFiles = [];
  }

  formatSize(bytes: number): string {
    if (bytes === 0) {
      return '0 B';
    }
    const k = 1000;
    const dm = 3;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  remove(event: Event, index: number): void {
    this.fileUpload.clearInputElement();
    this.fileUpload.onRemove.emit({originalEvent: event, file: this.fileUpload.files[index]});
    this.fileUpload.files.splice(index, 1);
  }

  upload(event: { files: any[]; }): void {
    this.fileService.uploadFiles(event.files).subscribe({
      next: (data) => {
        this.fileIds = data;
        this.refreshTimer = setInterval(() => { this.fetchUpdates(); }, 1000);
      },
      error: (err) => {
        this.messageService.add({severity: 'error', summary: 'Грешка', detail: err});
        console.error(err);
      }
    });
  }

  fetchUpdates(): void {
    this.fileService.getFileInfo(this.fileIds).subscribe({
      next: (files) => {
        this.resultFiles = files;
        let allFinished = true;
        this.resultFiles.forEach((item) => {
          switch (item.status) {
            case 1: item.severity = 'info'; allFinished = false; break;
            case 2: item.severity = 'warning'; allFinished = false; break;
            case 3: item.severity = 'success'; break;
            case 0: item.severity = 'error'; break;
            case 4: item.severity = 'error'; break;
          }
        });
        if (allFinished) {
          clearInterval(this.refreshTimer);
        }
      },
      error: (err) => {
        this.messageService.add({severity: 'error', summary: 'Грешка', detail: err});
      }
    });
  }

  download(): void {
    
  }

}
