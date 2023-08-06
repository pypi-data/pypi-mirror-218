interface ILoadDataModalInfo {
    total: number;
    curIndex: number;
}
declare class CommonStore {
    loadDataModalOpen: boolean;
    loadDataModalInfo: ILoadDataModalInfo;
    showCloudTool: boolean;
    setLoadDataModalOpen(value: boolean): void;
    setLoadDataModalInfo(info: ILoadDataModalInfo): void;
    setShowCloudTool(value: boolean): void;
    constructor();
}
declare const commonStore: CommonStore;
export default commonStore;
