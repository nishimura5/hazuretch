import pandas as pd

def interpolate(src_df, limit=None):
    if limit is None:
        limit = 5

    dst_df = src_df.interpolate(
        method='linear', 
        limit=limit,
        limit_direction='forward',
        limit_area='inside')

    ## interpolateだけだと埋めたくない行も埋まってしまうため、maskを追加
    ## たとえばlimit=3のとき、nanが4つ続いていても3個埋めてしまうので、maskでnanに埋め直す
    mask_df = pd.DataFrame()
    for col in src_df.columns:
        s = src_df[col].notnull()
        s = s.ne(s.shift()).cumsum()
        mask_df[col] = src_df.groupby([s, src_df[col].isnull()])[col].transform('size').where(src_df[col].isnull())
        dst_df[col] = dst_df[col].mask(mask_df[col]>limit)
   
    return dst_df

if __name__=="__main__":
    src_df = pd.read_csv('./test.csv', index_col='time')
    dst_df = interpolate(src_df, 3)
    print(dst_df)
