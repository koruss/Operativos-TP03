import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

import FileSystem from 'src/app/Models/file-system';
import FsChecker from 'src/app/Models/fs-checker';

@Injectable({
  providedIn: 'root'
})
export class FileSystemService {

  constructor(private httpClient: HttpClient) { }
  public async fsExists(hasFS: FsChecker): Promise<FsChecker>{
    return lastValueFrom(this.httpClient.post('/api/fs/check', hasFS));

  }

  public createFS(fsInfo: FileSystem): Promise<FileSystem> {
    return lastValueFrom(this.httpClient.post('/api/fs/create', fsInfo));
  }

}
