def render_cosmic_globe(orbit_map, df, title="🌍 3D Constellation Globe", mobile_mode=False):
    """
    تُنشئ كرة أرضية تفاعلية ثلاثية الأبعاد مع مسارات المدارات.
    """
    import numpy as np
    fig = go.Figure()
    
    # إضافة الكرة الأرضية
    fig.update_layout(
        geo=dict(
            projection_type='orthographic',
            showland=True,
            landcolor='rgb(10,10,20)',
            coastlinecolor='rgb(60,60,80)',
            showocean=True,
            oceancolor='rgb(5,5,15)',
            showcountries=True,
            countrycolor='rgb(50,50,70)',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400 if mobile_mode else 600,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    if not df.empty:
        # رسم مدارات الأقمار (خطوط)
        for name, orbit in list(orbit_map.items())[:30]:  # حد أقصى 30 مداراً للوضوح
            if not hasattr(orbit, 'position_at_time'):
                continue
            # توليد نقاط المدار (خطوة زمنية 0.1 لمدار كامل)
            orbit_points = []
            for t in np.linspace(0, orbit.period, 50):
                pos = orbit.position_at_time(t, apply_j2=True)
                if pos and len(pos) >= 3:
                    x, y, z = pos
                    r = math.sqrt(x**2 + y**2 + z**2)
                    if r == 0:
                        continue
                    lat = math.degrees(math.asin(z / r))
                    lon = math.degrees(math.atan2(y, x))
                    orbit_points.append((lon, lat))
            
            if len(orbit_points) > 1:
                lons, lats = zip(*orbit_points)
                fig.add_trace(go.Scattergeo(
                    lon=lons,
                    lat=lats,
                    mode='lines',
                    line=dict(width=1, color='rgba(0, 204, 255, 0.2)'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # رسم الأقمار (نقاط) كما هو موجود
        sample_size = min(100 if mobile_mode else 300, len(df))
        display_df = df.sample(n=sample_size) if len(df) > sample_size else df
        fig.add_trace(go.Scattergeo(
            lon=display_df['Longitude'].tolist(),
            lat=display_df['Latitude'].tolist(),
            mode='markers',
            marker=dict(
                size=6 if mobile_mode else 8,
                color=display_df['Status'].map({
                    '🟢 Active': '#00FF00',
                    '🟡 Calibration': '#FFAA00',
                    '🔴 Standby': '#FF5555',
                    '🔴 معطل': '#FF0000'
                }).tolist(),
                symbol='circle'
            ),
            text=display_df['Satellite'].tolist(),
            hoverinfo='text'
        ))
    
    # المحطة الأرضية
    fig.add_trace(go.Scattergeo(
        lon=[0],
        lat=[0],
        mode='markers',
        marker=dict(size=14, color='#FF3366', symbol='star'),
        text=['🛰️ Ground'],
        hoverinfo='text'
    ))
    
    return fig
