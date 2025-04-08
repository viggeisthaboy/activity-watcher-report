from aw_client import ActivityWatchClient
import pandas as pd
import plotly.express as px
from datetime import datetime, timezone, timedelta


def main():
    client = ActivityWatchClient()
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=1)

    bucket_name = 'aw-watcher-web-edge_REX'
    events = client.get_events(bucket_name, start=start_date, end=end_date)
    print(f"Found {len(events)} events")

    app_times = {}
    for event in events:
        app_name = event.data.get('title', 'Unknown')
        duration_seconds = event.duration.total_seconds()
        if app_name in app_times:
            app_times[app_name] += duration_seconds
        else:
            app_times[app_name] = duration_seconds

    # Create DataFrame and sort by duration
    pie_df = pd.DataFrame(list(app_times.items()), columns=['app_name', 'duration']).sort_values('duration',
                                                                                                 ascending=False)

    # Determine top 5 for labeling
    top_5 = pie_df.head(5)['app_name'].tolist()
    pie_df['text'] = pie_df.apply(
        lambda row: f"{row['app_name']}: {row['duration'] / pie_df['duration'].sum() * 100:.1f}%" if row[
                                                                                                         'app_name'] in top_5 else '',
        axis=1)

    # Pie chart
    pie_fig = px.pie(pie_df, names='app_name', values='duration')
    pie_fig.update_traces(
        text=pie_df['text'],
        textinfo='text',
        textposition='outside'
    )
    pie_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=True,
        showlegend=False
    )

    # Write pie chart to index.html with utf-8 encoding
    with open('C:/Users/vigge/.Coding/Moce-DV/Python/index.html', 'w', encoding='utf-8') as f:
        f.write(
            '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body style="margin:0;padding:0;">')
        f.write(pie_fig.to_html(include_plotlyjs=True, full_html=False, div_id='pie-chart',
                                config={'responsive': True}))
        f.write('<style>#pie-chart {width:100%;height:100vh;}</style>')
        f.write('</body></html>')
    print("Report generated successfully at C:/Users/vigge/.Coding/Moce-DV/Python/index.html")


if __name__ == '__main__':
    main()