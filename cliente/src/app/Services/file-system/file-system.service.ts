import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

import FileSystem from 'src/app/Models/file-system';
import FsChecker from 'src/app/Models/fs-checker';

@Injectable({
  providedIn: 'root'
})
export class FileSystemService {
  // private fsInfo: FileSystem= {
  //   sector_size: 0,
  //   sector_amount: 0,
  // }
  public fsChecker: FsChecker = {
    fs_exists: false,
  };

  constructor(private httpClient: HttpClient) { }

  async fsExists(): Promise<boolean>{
    this.httpClient.post('/api/fs/check', null).subscribe(data => {
      this.fsChecker = data;
    },
      error => {
        console.log(error);
      });
    console.log("sexo2");
    console.log(this.fsChecker.fs_exists);
    return this.fsChecker.fs_exists; 
  }

  public createFS(fsInfo: FileSystem): Promise<FileSystem> {
    return lastValueFrom(this.httpClient.post('/api/fs/create', fsInfo));
  }

}
