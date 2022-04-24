import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileService {

  constructor(private http: HttpClient) { }

  uploadFiles(files: any[]): Observable<number[]> {
    const formData = new FormData();
    for (const file of files) {
      formData.append(file.name, file);
    }
    return this.http.post<number[]>(`/api/hfntr/upload/`, formData);
  }

  getFileInfo(fileIds: number[]): Observable<any[]> {
    const ids = fileIds.join(',')
    return this.http.get<any[]>(`/api/hfntr/file/?id__in=${ids}`);
  }
  
  getStatus(fileId: number): Observable<number> {
    return this.http.get<number>(`/api/hfntr/status/${fileId}/`);
  }

  getDownloadUrl(fileId: number):  Observable<string> {
    return this.http.get<string>(`/api/hfntr/download/${fileId}/`);
  }
}
